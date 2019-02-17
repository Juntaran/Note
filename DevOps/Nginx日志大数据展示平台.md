# Nginx 日志大数据展示平台

**实时** 展示业务的请求，包括但不限于 qps、延迟、状态码等指标能够帮助业务快速分析定位问题，如何实时展示 MIUI 业务请求数据，如何在 SRE 出去玩的时候 DEV 可以快速自查服务问题 : ) 是我们做这个项目的起因  



## 1 技术选型

先说结论：我们选择了 Druid 作为大数据实时分析  

再说为什么：Elasticsearch 是一个基于 apache lucene 的搜索引擎，提供了 schema-free 模式的全文搜索同事提供了访问原始事件级别的数据，但是 Elasticsearch 在数据汇总方面要求更多的存储资源；Druid 侧重于 OLAP 工作流程，在低成本的基础上对高性能进行了很多优化，并提供了对结构化的时间数据的一些基本的搜索支持  

Elasticsearch 的存储结构是 Lucene 索引 + 文档数据，而 Druid 则是 bitmap 索引 + metric/timestamp 的压缩，它的索引根据时间进行分片，在查询的时候根据事件进行索引查询  

量级小一些的业务完全可以通过 ELK 这一套来展示，但是当业务数据量极大地时候，ELK 很难满足我们的需求，而因此我们选择了 Druid   

## 2 FAST 平台设计

这个 MIUI Nginx 数据展示平台我们称之为 *FAST* 平台  ![Fast](http://juntaran.me/ftp/pictures/Fast.png)

（图源网络，侵删）  

既然 OLAP 选用了 Druid，那么我们怎么把每台 Nginx 实例的日志数据实时打入到 Druid 呢？这里我们总共分为了三个阶段

### 2.1.1 阶段一 

在初始阶段，我们的数据流向如下：

```
Fluentd → Talos → Kafka → 中间件 → Kafka → Druid 
```

 为了便于我们日常排障，我们并没有让 Nginx 直接输出 json 格式日志，而是保留原始日志，使用 Fluentd 上报到小米数据流总线 [Talos](http://docs.api.xiaomi.com/talos/) 之后通过 Kafka Sink 读取出来，使用一个中间件进行数据处理、过滤、转换，再打到 Kafka 里，因为 Druid 支持 Kafka 数据源，因此这个流程到此就终止了  

这里值得一说的是为什么需要存在中间件这个东西，首先 Druid 支持的数据格式是 json 格式，因此我们需要把原始日志进行转换；其次 Druid 存在一个维度爆炸的问题，维度取值太多（比如 user_id, ip）一般是维度爆炸的根源，会对系统的性能造成巨大的影响，因此我们要对维度取值进行裁剪  

我们是这样定义 Druid 维度规则的：

> scheme
>
> http_host
>
> request_uri
>
> hostname
>
> status

其中，hostname 和 request_uri 是极易引起维度爆炸的因素，因为有些 Nginx 实例是部署在 Kubernetes 上的，所以 hostname 会取值过多；request_uri 更不必说，不同的业务 request_uri 命名更不相同，更何况其中还会存在数据 id、uuid 这些变量过大的因素  

但是我们还要保留 request_uri ，这样可以快速查询到是哪个路径存在问题，方便研发定位问题，因此我们进行了数据裁剪  

中间件根据小米机房 ip 借鉴 Nginx 源码构建了一颗 radix tree，能够快速判断该 ip 所属机房，这样 hostname 字段便替换成了机房名；而 request_uri 的解决方案更为复杂  

我一开始默认最多保留 2 个 / 的内容，但是这样很不明确，不方便快速排查问题，而且有些业务也存在了在前 2 个 / 中就包含了资源 ID 的情况  

之后我创建了一个规则，中间件进行了正则匹配，匹配规则则是 **全业务** 通用，能够在最大程度上保留有用信息而不会对系统性能造成影响  

### 2.2.2 阶段二

第一阶段支撑了 FAST 平台一段时间，但是随着接入业务的增加，成本是一个问题  

```Fluentd → Talos → Kafka → 中间件 → Kafka → Druid ```

这个流程中，Talos 可以视为 Kafka ，根据三副本原则，接入业务的 Nginx 日志可能会保存 9 份不止，极大地浪费了数据流资源，因此我在阶段二修改了中间件，第一阶段的中间件是采用 Go 语言编写，从 Kafka 的 源 Topic 读取数据再转发回 Kafka 的目的 Topic，第二阶段我修改了这部分代码  

```
Fluentd → Talos → 中间件 → Kafka → Druid
```

用 Scala 重写了中间件，使用 Spark-Streaming 从 Talos 读取数据再经处理后打入到 Kafka，这样可以节约近 1/3 的数据流资源

### 2.2.3 阶段三

阶段三也就是现在的阶段，我们认为阶段二这一套流程

```Fluentd → Talos → 中间件 → Kafka → Druid```

还是有些浪费资源，那么如何节约资源呢？因此我用 Go 重写了一个简易版本的 Fluentd 就叫它 Enlc (EasyNginxLogCollector) 好了，整个数据流向变成了如下所示：

```Enlc → Talos → Druid```

（这也由于数据流团队给力的改进，对 Talos 增加了 Druid 可以减少一部分 Kafka 资源）  

Enlc 在每台 Nginx 实例上根据规则抓取对应的 Nginx 日志，并进行数据处理转发，也就是说在打入 Talos 之前，数据便已经是 Druid 可以接受的了，直接砍掉了后续的 **读取 → 处理 → 转发** 的过程



## 3 Enlc 的实现

### 3.1 组件原理

实现原理参考 LogStash、Fluentd、Filebeat  

整个项目可以分为 5 个阶段：

```Collector → Harvester → Decorator → Spooler → Publisher ```

1. *Collector* 对配置进行了一系列的解析，总体原则就是对每个目的 Topic 分别创建一组 *Harvester, Spooler, Publisher* 

2. 接下来每个 *Harvester* 读取一个文件，类似于 **tail -f** 一样，把每一行新增的日志发送给 *Decorato*  

3. *Decorator* 顾名思义就是数据格式转换，它的功能可以参考阶段一，它接收 *Harvester* 发来的日志，之后把他发给 *Spooler*，*Decorator* 会根据配置文件中的规则进行匹配，**Enlc** 相比于第一阶段还有一个优点，那就是它的配置可以由各个业务自定义，第一阶段我已经用加粗说明了，它的配置文件需要全业务通用，而 Enlc 不同，每个业务有自己的 Nginx 集群，可以根据各个业务来配置相应的规则，完全做到客制化     

4. *Spooler* 的存在还是有必要提一句的，可能会问了， *Decorator* 发过来直接转发到 Talos 不就好了，为什么要多加一层 *Spooler* 呢？*Spooler* 可以理解成一个缓冲队列，*Spooler* 什么时候处理这个队列有两个方案：1. 每隔一段时间处理一次 2. 队满则处理，这样的好处是可以成批处理待转发的数据，不必每一条都调用一下 *Pubisher*

5. *Publisher* 的功能就很简单了，收到 *Spooler* 发给他的一批数据，*Rua* 一下的发给 Taolos 然后我们的任务就完成了  

6. 还有一些杂乱的处理，比如如果 Enlc 被 kill 了会怎么办？enlc 其实是做了一个信号收集，如果接收到 kill 等信号，会直接保存当前读取的日志进度到 `/tmp/offset.pos` 文件中，这样下次开启会继续读取。但是这样就会存在一个问题，如果一个业务量特别大的业务，Enlc 停止了 几小时后又启动了起来，它读取的任务就很艰巨了，而 Druid 只接收近 10min 的数据，所以从记录的位置开始读取是没有太大意义的，**就算 Enlc 读了上报， Druid 也不会接收，反而会导致这台机器资源紧缺影响到 Nginx**，因此这个配置虽然存在，我把它默认关闭了，如果需要开启可以直接注释 [这里](https://github.com/Juntaran/EzNginxLogCollector/blob/7ac6e3f02ab38557e3ce315c0270063e3ce0594a/common/collector/collector.go#L134) 的 `offset = 0`  再比如说如果有某些特殊原因，Enlc 挂了，Enlc 没有像其他日志收集组件那样实时记录 offset，那么 Enlc 会不会丢数据？答案是会的，因为业务 Nginx 机器的负载最重要，不能让 Enlc 占用过多的资源，如果有过多的日志让堆积让 Enlc 转发，那么它一定会影响业务，占用过多的 Cpu 导致 load 升高，而且这部分日志 Druid 也不会接收所以就算打上去了也没有用



### 3.2 配置文件

详见注释

```yaml
nginxlogpath:
  - path: /home/juntaran/Workspace/goWorkspace/src/github.com/Juntaran/EzNginxLogCollector/tests/tests1
    file:
      - collect_1*.log
      - collect_2*.log
    topic: test1
  - path: /home/juntaran/Workspace/goWorkspace/src/github.com/Juntaran/EzNginxLogCollector/tests/tests2
    file:
      - collect_1*.log
      - collect_2*.log
    topic: test2

nginxpospath: /tmp/offset.pos	# enlc 如果被 kill 会在退出之前记录当前读取文件的进度到这个文件

# Decorator 是按照这个规则处理的
nginxlogfmt:  $http_host\t$server_addr\t$hostname\t$remote_addr\t$http_x_forwarded_for\t$time_local\t$request_uri\t$request_time\t$status\t$upstream_addr\t$upstream_response_time\t$scheme  

filterpattern:
  - ^\d+$						# 过滤规则1：如果有一段为纯数字，则其与其后皆删除
  - ^\w{8}(-\w{4}){3}-\w{12}$	# 过滤规则2：如果有一段为 uuid，则其与其后皆删除

decorate:
  buffer: 10240					# decorate  缓冲大小
  worker: 20					# decorator goroutine 数

spool:
  spoolsize: 1000				# spool 缓冲区大小，满了则打入 publisher
  flushtime: 1					# 每隔 flushtime 则打入 publisher

publish:
  timeout: 5					# 上报超时配置
  worker: 10					# publisher gouroutine 数

loglevel: error					# 日志等级，可选 debug、info、warn、error、fatal、panic
```



### 3.3 对比

以下放几张 Enlc 和 Fluentd 的性能对比图:   

在大多数情况下，Enlc 所占用的内存和 Cpu 都小于 Fluentd  

推荐使用如下命令启动：

```bash
nice -n 19 ./EzNginxLogCollector_linux_amd64 > enlc.log 2>&1 & 
```





![Fluentd vs Enlc](http://juntaran.me/ftp/pictures/fluentd-vs-enlc.png)



Enlc 简易版的代码可以参考 [GayHub](https://github.com/Juntaran/EzNginxLogCollector)
