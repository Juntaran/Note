

# HBS

Hbs(heart-beat server) 提供给 Agent 和 Judge 的接口都是 json rpc



## 1 职责

1.1 处理 Agent 心跳请求，填充 host 表

​	策略配置 web 端(Portal 模块)，存在 group 概念，对机器进行了分组，portal 数据库中有一个 host 表，存放了机器信息(hostname、ip、agent 版本、插件版本)。agent 每分钟调用一次 hbs rpc 接口发送一个心跳包，发送一些信息（agent版本、插件版本）给 hbs，hbs 写入数据库

1.2 将 IP 白名单分发到所有 Agent

​	Agent 存在一个 http 的 run 接口，可以接受发送过来的 shell 指令在本机执行，比较危险，所以增加了白名单，只有在白名单里的机器发送的指令才会被执行（Hbs 配置中的 trustable ips）, Agent 每分钟调用一下 Hbs rpc 接口获取授信的 IP 列表 

```json
"trustable": [""],
```

1.3 告诉各个 Agent 需要执行哪些插件

​	Agent  采集信息可能不够用，所以允许用户编写采集脚本，对 Agent 功能进行扩展。Agent 配置中含有了 get repo 地址，调用 Agent http 接口(plugin update 接口)可以触发 Agent 主动去 `git pull` ，这就意味所有的机器都 clone 了所有脚本。哪些 Agent 需要执行哪些插件，这个信息是在 portal 中进行配置的，通过 Hbs 分发给 Agent

1.4 告诉各个 Agent 需要监听哪些端口、进程

​	一个机器上监听的端口和进程可能特别多，不适合 falcon Agent 自动采集所有的信息上报，用户不太需要关注所有的上报。之后改成了只有用户配置的端口和进程我们才会采集统计。Agent 如何知道自己需要采集哪些端口、进程，则是由 Hbs 通知的

1.5 缓存监控策略

​	Judge(报警组件)需要获取所有的报警策略，Judge 读取 Portal 的数据库是不好的，因为 judge 的实例数可能有很多，对 Portal 数据库的压力比较大，既然根据以上几个需求，Hbs 都需要访问 Portal 的数据库，那就让 Hbs 也干了获取报警策略的活，获取报警策略缓存到内存里，之后 Judge 向 Hbs 发起请求，这样就会大大减小对 Portal 数据库的压力，此时 Hbs 就相当于 Portal 的一个 cache



## 2 配置说明

```yaml
{
    "debug": true,
    "database": "root:password@tcp(127.0.0.1:3306)/falcon_portal?loc=Local&parseTime=true", # Portal的数据库地址
    "hosts": "", # portal数据库中有个host表，如果表中数据是从其他系统同步过来的，此处配置为sync，否则就维持默认，留空即可
    "maxIdle": 100,
    "listen": ":6030", # hbs监听的rpc地址
    "trustable": [""],
    "http": {
        "enabled": true,
        "listen": "0.0.0.0:6031" # hbs监听的http地址
    }
}
```



## 3 代码结构

```shell
.
├── LICENSE
├── NOTICE
├── README.md
├── cache
│   ├── agents.go
│   ├── cache.go
│   ├── expressions.go
│   ├── groups.go
│   ├── hosts.go
│   ├── plugins.go
│   ├── strategies.go
│   └── templates.go
├── cfg.example.json
├── control
├── db
│   ├── agent.go
│   ├── db.go
│   ├── expression.go
│   ├── group.go
│   ├── host.go
│   ├── plugin.go
│   ├── strategy.go
│   └── template.go
├── g
│   ├── cfg.go
│   └── g.go
├── http
│   ├── common.go
│   ├── http.go
│   └── proc.go
├── main.go
└── rpc
    ├── agent.go
    ├── hbs.go
    └── rpc.go
```



## 4 查询缓存

Agent 和 Judge 模块都通过 Hbs 来读取用户配置信息，Hbs 周期性的读取 Protal DB 的内容缓存到内存中

Agent 每分钟发送心跳、询问需要监听哪些端口、统计哪些进程、执行哪些插件，同时拿到授信 IP 列表

Judge 请求 Hbs 拿到 expression 列表、strategy 列表

Hbs 则周期性读取 Portal DB 的内容，缓存到内存中，Agent、Judge 直接返回内存中的数据



### 4. db/agent.go

___

我们更能要通过 Agent 更新数据库中的 Host 表，Host 表会根据配置进行不同的处理

如果配置中 Host 为空，则 Hbs 会进行插入操作，插入 hostname, ip, agent_version, plugin_version，其中 hostname 为唯一索引，如果数据库中已经有了相同的 hostname ，则进行更新，使用了 duplicate key

如果配置成了 `sync` 等非空字符，则根据 hostname 更新 Host 表的 ip, agent_version, plugin_version

hostname 其实是 Agent 执行了 `hostname` 这条指令，ip 则是进行探测，可能会有多个 ip，因此选择 hostname 作为唯一索引



### 4.2 db/host.go...

___

1. 准备一些数据结构
2. 填充这些数据结构
3. 准备一些查询语句等待上层业务来查询



### 4.3 rpc/hbs.go

___

GetExpressions() GetStrategies() 两个方法是为 Judge 模块准备的两个 rpc 方法

GetExpressions() 获得所有的策略表达式

GetStrategies() 获得所有的策略



当 Judge 调用 GetExpressions() ，传入 req model.NullRpcRequest (一个空的 struct), reply *model.ExpressionResponse（一个 Expression 列表）

之后直接从缓存中读取 Expression 返回给 reply.Expressions

```go
reply.Expressions = cache.ExpressionCache.Get()
```

```go
func (this *SafeExpressionCache) Get() []*model.Expression {
	this.RLock()
	defer this.RUnlock()
	return this.L
}
```

而这些是在 Init() 中就已经填充好的

```go
// 从 db 查询所有的 expression
func (this *SafeExpressionCache) Init() {
	es, err := db.QueryExpressions()
	if err != nil {
		return
	}

	this.Lock()
	defer this.Unlock()
	this.L = es
}
```



### 4.4 Plugin 完整的逻辑

___

`rpc/agent.go` 包含了 MinePlugins() 和 ReportStatus() 给 Agent 使用

```go
func (t *Agent) MinePlugins(args model.AgentHeartbeatRequest, reply *model.AgentPluginsResponse) error {
	if args.Hostname == "" {
		return nil
	}
	// 获取 plugin 列表
	reply.Plugins = cache.GetPlugins(args.Hostname)
	reply.Timestamp = time.Now().Unix()

	return nil
}
```

args 包含了 hostname， Hbs 根据 hostname 返回对应的 plugin 列表

之后使用 cache.GetPlugins() 填充 reply.Plugins

```go
// 根据 hostname 获取关联的插件
func GetPlugins(hostname string) []string {
	hid, exists := HostMap.GetID(hostname)
	if !exists {
		return []string{}
	}

	gids, exists := HostGroupsMap.GetGroupIds(hid)
	if !exists {
		return []string{}
	}

	// 因为机器关联了多个 Group，每个 Group 可能关联多个 Plugin，故而一个机器关联的 Plugin 可能重复
	pluginDirs := make(map[string]struct{})
	for _, gid := range gids {
		plugins, exists := GroupPlugins.GetPlugins(gid)
		if !exists {
			continue
		}

		for _, plugin := range plugins {
			pluginDirs[plugin] = struct{}{}
		}
	}

	size := len(pluginDirs)
	if size == 0 {
		return []string{}
	}

	dirs := make([]string, size)
	i := 0
	for dir := range pluginDirs {
		dirs[i] = dir
		i++
	}

	sort.Strings(dirs)
	return dirs
}
```

```go
// 一个机器可能在多个 group 下，做一个map缓存 hostid 与 groupid 的对应关系
type SafeHostGroupsMap struct {
	sync.RWMutex
	M map[int][]int
}
```

cache.GetPlugins() 的逻辑如下

1. 根据 hostname 寻找所属的 hostId（`hid, exists := HostMap.GetID(hostname)`，HostMap 也是一个内存中的结构，并不是实时访问数据库的，HostMap 也是在 cache.go 中的 `HostMap.Init()` 初始化的，并一分钟更新一次）
2. 根据 hostId 寻找所属的 group（`gids, exists := HostGroupsMap.GetGroupIds(hid)`，HostGroupMap 也是一个内存中的结构，并不是实时访问数据库的，HostMap 也是在 cache.go 中的 `HostGroupsMap.Init()` 初始化的，并一分钟更新一次）
3. 根据查出的 gid 列表，取出所有的 plugins （`GroupPlugins.GetPlugins(gid)`，同上 GroupPlugins 也是在 cache.go 中 `GroupPlugins.Init()` 进行初始化的，同样也是一分钟更新一次）
4. 因为机器关联了多个 Group，每个 Group 可能关联多个 Plugin，故而一个机器关联的 Plugin 可能重复，所有的 plugins 信息放到 `pluginDirs := make(map[string]struct{})` 中，此时利用 map 来去重，然后便利 pluginDirs 这个 map ，取出所有的 key 也就是去重后的 plugin 列表写入 dirs，之后对 dirs 排序后返回



## 5 Strategy 的完整逻辑

strategy 与 plugin 类似，只是更为复杂

1. main.go 里 cache.Init() 中进行了 `TemplateCache.Init()` 和 `Strategies.Init(TemplateCache.GetMap())` 并且定时 1分钟执行一次

   1.1 `TemplateCache.Init()` 则是获取所有的策略模版列表，填充并返回一个 `map[int]*model.Template` 的 map ，map 的 value 中包含了模板表 Id, Name, ParentId, ActionId, Creator，map 的 key 是模板在模板表的Id ，之后把这个 map 写入全局变量 `TemplateCache`

   1.2 `Strategies.Init(TemplateCache.GetMap())` 传入了`TemplateCache.Init()` 写入全局变量 `TemplateCache` 中的 map ，根据这个 map 查询数据库 `db.QueryStrategies(tpls)` ，这个 map 包含了所有的模板ID 以及模板内容    

   ​		1.2.1 在 `db/strategy.go` 里的 `QueryStrategies()` 函数中，先查询所有的策略信息，之后根据传入的 map 进行匹配，如果查出来的 Strategy 没有对应的模板，那就没有 action，就没法报警，无需往后传递了，之后 db.QueryStrategies() 返回一个 map `map[int]*model.Strategy` ，该 map key 是策略ID，value 是策略内容

   ​		1.2.2 `cache.go` 中的 `Strategies.Init(TemplateCache.GetMap())` 方法把之前查出的策略 map 写入全局变量 `Strategies` 中的 map

2. `cache/strategies.go` 中的 `GetBuiltinMetrics()` 函数，会被 `rpc/agent.go` 中的 `BuiltinMetrics()` 方法调用

   2.1 首先，获取 hostId ，根据 hostname 寻找所属的 hostId（`hid, exists := HostMap.GetID(hostname)`，HostMap 也是一个内存中的结构，并不是实时访问数据库的，HostMap 也是在 cache.go 中的 `HostMap.Init()` 初始化的，并一分钟更新一次）

   2.2 根据 hostId 寻找所属的 group（`gids, exists := HostGroupsMap.GetGroupIds(hid)`，HostGroupMap 也是一个内存中的结构，并不是实时访问数据库的，HostMap 也是在 cache.go 中的 `HostGroupsMap.Init()` 初始化的，并一分钟更新一次）

   2.3 根据 gids，获取绑定的所有 tids，因为机器可能关联了多个 Group，每个 Group 可能关联多个 Template，可能会重复，因此在这里使用了 set 去重，`tidSet := set.NewIntSet()` ，根据查出的 gid 列表，取出所有的 templates （`GroupTemplates.GetTemplateIds(gid)`，同上 GroupTemplates 也是在 cache.go 中 `GroupTemplates.Init()` 进行初始化的，同样也是一分钟更新一次），之后把 tidSet 转换成 slice `tidSlice := tidSet.ToSlice()`。

   2.4 然而还没完，获取所有的模板  `allTpls := TemplateCache.GetMap()`， 同上，template 在 `cache.go` 中的 `TemplateCache.Init()` 之前已经定时更新好了，把 2.3 查出的 template 放到 `ParentIds(allTpls, tid)` 函数中查找他们的父模版，此处最大深度是 10，超过 10 就会直接返回。之后把所有的模板以及他们的父模板放到 set 里去重，并转换回 slice `tidSlice = tidSet.ToSlice()`

   2.5 把所有相关的模版 id 用逗号拼接，开始查库 `db.QueryBuiltinMetrics(strings.Join(tidStrArr, ","))`，查询相关模版内，metric 为 `net.port.listen, proc.num, du.bs, url.check.health ` 的结果，返回 `[]*model.BuiltinMetric` 结构的数据

   2.6 `rpc/agent.go ` 中的 `BuiltinMetrics()` 方法存在 md5 校验



## 6 Agent 的心跳上报

在 `agent/cron/report.go` 中，`ReportAgentStatus()` 会调用 `reportAgentStatus()` ，该函数根据根据 Agent 的配置，每 60s 通过 rpc 连接 Hbs 上报 Hostname, IP, AgentVersion, PluginVersion

```go
g.HbsClient.Call("Agent.ReportStatus", req, &resp)
```

也就是调用 `hbs/rpc/agent.go` 中的 `ReportStatus()` 方法  

该方法调用了 `cache.Agents.Put()` 方法，把所有的信息放入内存 cache，之后写入数据库

这里每个 Agent 心跳一次无需立刻更新数据库，Falcon 的逻辑是把他们缓存在内存，每隔 1h 写一次 DB





## 7 问题

1. BuiltinMetric 只有内建 metric(net.port.listen, proc.num, du.bs, url.check.health) 吗

   —— Agent 查询 Hbs 这些内容哪些需要监控

2. 用户自定义的 metric 怎么查

   —— 除了上述都是 Agent 自己来查











