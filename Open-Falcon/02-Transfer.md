# Transfer

Transfer 是数据转发服务。它接收 Agent 上报的数据，然后按照哈希规则进行数据分片、并将分片后的数据分别 push 给 graph&judge 等组件，也会根据配置打向 tsdb



## 1 配置说明

```yaml
    debug: true/false, 如果为true，日志中会打印debug信息

    minStep: 30, 允许上报的数据最小间隔，默认为30秒

    http
        - enabled: true/false, 表示是否开启该http端口，该端口为控制端口，主要用来对transfer发送控制命令、统计命令、debug命令等
        - listen: 表示监听的http端口

    rpc
        - enabled: true/false, 表示是否开启该jsonrpc数据接收端口, Agent发送数据使用的就是该端口
        - listen: 表示监听的http端口

    socket #即将被废弃,请避免使用
        - enabled: true/false, 表示是否开启该telnet方式的数据接收端口，这是为了方便用户一行行的发送数据给transfer
        - listen: 表示监听的http端口

    judge
        - enabled: true/false, 表示是否开启向judge发送数据
        - batch: 数据转发的批量大小，可以加快发送速度，建议保持默认值
        - connTimeout: 单位是毫秒，与后端建立连接的超时时间，可以根据网络质量微调，建议保持默认
        - callTimeout: 单位是毫秒，发送数据给后端的超时时间，可以根据网络质量微调，建议保持默认
        - pingMethod: 后端提供的ping接口，用来探测连接是否可用，必须保持默认
        - maxConns: 连接池相关配置，最大连接数，建议保持默认
        - maxIdle: 连接池相关配置，最大空闲连接数，建议保持默认
        - replicas: 这是一致性hash算法需要的节点副本数量，建议不要变更，保持默认即可
        - cluster: key-value形式的字典，表示后端的judge列表，其中key代表后端judge名字，value代表的是具体的ip:port

    graph
        - enabled: true/false, 表示是否开启向graph发送数据
        - batch: 数据转发的批量大小，可以加快发送速度，建议保持默认值
        - connTimeout: 单位是毫秒，与后端建立连接的超时时间，可以根据网络质量微调，建议保持默认
        - callTimeout: 单位是毫秒，发送数据给后端的超时时间，可以根据网络质量微调，建议保持默认
        - pingMethod: 后端提供的ping接口，用来探测连接是否可用，必须保持默认
        - maxConns: 连接池相关配置，最大连接数，建议保持默认
        - maxIdle: 连接池相关配置，最大空闲连接数，建议保持默认
        - replicas: 这是一致性hash算法需要的节点副本数量，建议不要变更，保持默认即可
        - cluster: key-value形式的字典，表示后端的graph列表，其中key代表后端graph名字，value代表的是具体的ip:port(多个地址用逗号隔开, transfer会将同一份数据发送至各个地址，利用这个特性可以实现数据的多重备份)

    tsdb
        - enabled: true/false, 表示是否开启向open tsdb发送数据
        - batch: 数据转发的批量大小，可以加快发送速度
        - connTimeout: 单位是毫秒，与后端建立连接的超时时间，可以根据网络质量微调，建议保持默认
        - callTimeout: 单位是毫秒，发送数据给后端的超时时间，可以根据网络质量微调，建议保持默认
        - maxConns: 连接池相关配置，最大连接数，建议保持默认
        - maxIdle: 连接池相关配置，最大空闲连接数，建议保持默认
        - retry: 连接后端的重试次数和发送数据的重试次数
        - address: tsdb地址或者tsdb集群vip地址, 通过tcp连接tsdb.
```



## 2 主要流程

`transfer/main.go` 大致流程依旧是先解析参数配置，之后执行以下几个函数

```go
proc.Start()

sender.Start()
receiver.Start()

http.Start()
```



### 2.1 proc.Start()

`proc.Start()` 只是打印了一个 Start，在函数执行之前，还初始化了很多全局变量，比如 `RecvDataFilter, RecvDataTrace` 在 `transfer/sender/sender.go` 和 `transfer/http/proc_http.go` 中使用 

此外还有一些统计指标的全局变量在这里初始化，详见 `transfer/proc/proc.go`



### 2.2 sender.Start()

`sernder.Start()` 根据配置初始化了一些默认参数、连接池、发送队列、环形队列

初始化完以上基础组建后，启动 SendTasks

```go
// 默认参数
var (
	MinStep int //最小上报周期,单位sec
)

// 服务节点的一致性哈希环
// pk -> node
var (
	JudgeNodeRing *rings.ConsistentHashNodeRing
	GraphNodeRing *rings.ConsistentHashNodeRing
)

// 发送缓存队列
// node -> queue_of_data
var (
	TsdbQueue   *nlist.SafeListLimited
	JudgeQueues = make(map[string]*nlist.SafeListLimited)
	GraphQueues = make(map[string]*nlist.SafeListLimited)
)

// 连接池
// node_address -> connection_pool
var (
	JudgeConnPools     *backend.SafeRpcConnPools
	TsdbConnPoolHelper *backend.TsdbConnPoolHelper
	GraphConnPools     *backend.SafeRpcConnPools
)

// 初始化数据发送服务, 在main函数中调用
func Start() {
	// 初始化默认参数
	MinStep = g.Config().MinStep
	if MinStep < 1 {
		MinStep = 30 //默认30s
	}
	// 初始化基础组件
	initConnPools()
	initSendQueues()
	initNodeRings()
	// SendTasks依赖基础组件的初始化,要最后启动
	startSendTasks()
	startSenderCron()
	log.Println("send.Start, ok")
}
```

- 创建连接池的时候，judge 集群循环获取 Judge 集群的每一个 node，生成一个 node 连接池

- graph  集群循环集群中的每隔 node，每个 node 可能有多个主机地址，去重后得到一个连接池


- judge 根据每个 node 创建一个 safe list
- graph 两层循环拼接成 node+addr，再创建一个 safe list
- tsdb 创建一个 safe list



- 调用 `initNodeRing` 创建一致性 hash 环时，获取了 judge 和 graph 的 node 名称，根据名称生成 hash 值后生成环



- 调用 `startSendTasks` 发送数据时，对于 judge，循环每个 judge node 队列中的数据，将其发送到对应 node 的 graph node 队列，将循环该 node 列表中的所有地址，每个地址接收一份数据，同一份数据被复制了 `len(node.addr)` 份发送



`"falcon-plus/common/model" ` 定义了 `MetaData` 结构体

```go
type MetaData struct {
	Metric      string            `json:"metric"`
	Endpoint    string            `json:"endpoint"`
	Timestamp   int64             `json:"timestamp"`
	Step        int64             `json:"step"`
	Value       float64           `json:"value"`
	CounterType string            `json:"counterType"`
	Tags        map[string]string `json:"tags"`
}
```

MetaData 包含转 String() 与 PK() 方法，String() 则是返回格式化字符串，PK() 则是对传入的 tags 排序后返回格式化字符串



### 2.3 receiver.Start()

```go
func Start() {
	go rpc.StartRpc()
	go socket.StartSocket()
}
```

根据配置分别开启 rpc 和 tcp 服务监听指定的端口



## 2.4 http.Start()

调用 startHttpServer() 函数，先根据配置看是否开启 http 监听

之后

```go
// 开启基础监听路径 /health /version /workdir /config /config/reload 
configCommonRoutes()
// 监听统计指标路径 /counter/all 等 
configProcHttpRoutes()
// 监听 debug 路径 /debug/connpool/ 
configDebugHttpRoutes()
// 监听 api /api/push
configApiRoutes()
```







