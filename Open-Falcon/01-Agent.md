

# Agent

Agent 用于采集机器负载监控指标，比如 cpu.idle、load.1min、disk.io.util 等等，每隔 60 秒 push 给 Transfer。Agent 与 Transfer 建立了长连接，数据发送速度比较快，Agent 提供了一个 http 接口 `/v1/push` 用于接收用户手工 push 的一些数据，然后通过长连接迅速转发给 Transfer



## 1 配置说明

```yaml
{
    "debug": true,  # 控制一些debug信息的输出，生产环境通常设置为false
    "hostname": "", # agent采集了数据发给transfer，endpoint就设置为了hostname，默认通过`hostname`获取，如果配置中配置了hostname，就用配置中的
    "ip": "", # agent与hbs心跳的时候会把自己的ip地址发给hbs，agent会自动探测本机ip，如果不想让agent自动探测，可以手工修改该配置
    "plugin": {
        "enabled": false, # 默认不开启插件机制
        "dir": "./plugin",  # 把放置插件脚本的git repo clone到这个目录
        "git": "https://github.com/open-falcon/plugin.git", # 放置插件脚本的git repo地址
        "logs": "./logs" # 插件执行的log，如果插件执行有问题，可以去这个目录看log
    },
    "heartbeat": {
        "enabled": true,  # 此处enabled要设置为true
        "addr": "127.0.0.1:6030", # hbs的地址，端口是hbs的rpc端口
        "interval": 60, # 心跳周期，单位是秒
        "timeout": 1000 # 连接hbs的超时时间，单位是毫秒
    },
    "transfer": {
        "enabled": true, 
        "addrs": [
            "127.0.0.1:18433"
        ],  # transfer的地址，端口是transfer的rpc端口, 可以支持写多个transfer的地址，agent会保证HA
        "interval": 60, # 采集周期，单位是秒，即agent一分钟采集一次数据发给transfer
        "timeout": 1000 # 连接transfer的超时时间，单位是毫秒
    },
    "http": {
        "enabled": true,  # 是否要监听http端口
        "listen": ":1988",
        "backdoor": false
    },
    "collector": {
        "ifacePrefix": ["eth", "em"], # 默认配置只会采集网卡名称前缀是eth、em的网卡流量，配置为空就会采集所有的，lo的也会采集。可以从/proc/net/dev看到各个网卡的流量信息
        "mountPoint": []
    },
    "default_tags": {
    },
    "ignore": {  # 默认采集了200多个metric，可以通过ignore设置为不采集
        "cpu.busy": true,
        "df.bytes.free": true,
        "df.bytes.total": true,
        "df.bytes.used": true,
        "df.bytes.used.percent": true,
        "df.inodes.total": true,
        "df.inodes.free": true,
        "df.inodes.used": true,
        "df.inodes.used.percent": true,
        "mem.memtotal": true,
        "mem.memused": true,
        "mem.memused.percent": true,
        "mem.memfree": true,
        "mem.swaptotal": true,
        "mem.swapused": true,
        "mem.swapfree": true
    }
}
```

 

## 2 Agent 的结构

| 目录    | 作用                                     |
| ------- | ---------------------------------------- |
| cron    | 每隔一段时间要执行的代码都在这里         |
| func    | 采集信息函数                             |
| g       | global目录，全局都会用到的东西           |
| http    | 一个http的server，获取单机指标的一些数值 |
| plugins | 插件                                     |
| public  | 静态资源文件                             |



## 3 执行流程

`agent/main.go` 如下



```go
func main() {

	// 读参数
	cfg := flag.String("c", "cfg.json", "configuration file")
	version := flag.Bool("v", false, "show version")
	check := flag.Bool("check", false, "check collector")

	flag.Parse()

	if *version {
		fmt.Println(g.VERSION)
		os.Exit(0)
	}

	if *check {
		funcs.CheckCollector()
		os.Exit(0)
	}

	g.ParseConfig(*cfg)         // 解析参数

	// 初始化全局变量
	if g.Config().Debug {		// 设置日志级别
		g.InitLog("debug")
	} else {
		g.InitLog("info")
	}

	g.InitRootDir()				// 获取当前路径
	g.InitLocalIp()				// 连接 hbs 同时获取本地连接
	g.InitRpcClients()			// 根据配置决定是否初始化 hbs client	
	funcs.BuildMappers()        // funcs里是采集信息函数

	go cron.InitDataHistory()	// 不断检查 cpu、磁盘状态

	// 以下四行与心跳相关
	cron.ReportAgentStatus()    // 汇报agent状态
	cron.SyncMinePlugins()      // 同步我要执行的插件
	cron.SyncBuiltinMetrics()   // 同步 metric
	cron.SyncTrustableIps()     // 获取内置ip

	// 收集信息
	cron.Collect()

	// 默认1988端口
	go http.Start()

	select {}

}
```



## 4 与 Hbs 的联系

在 `cfg.json` 中决定是否开启 heartbeat，`agent/main.go` 中会调用 `g.InitRpcClients()` ，如果启动 heartbeat，会创建一个 `*SingleConnRpcClient` 类型的全局变量 `HbsClient` 

```go
HbsClient = &SingleConnRpcClient{
	RpcServer: Config().Heartbeat.Addr,
	Timeout:   time.Duration(Config().Heartbeat.Timeout) * time.Millisecond,
}
```



### 4.1 心跳上报

`cron.ReportAgentStatus()` 上报心跳，根据配置设置的间隔时间，执行 `agent/cron/reporter.go` 中的 `reportAgentStatus()` 函数，上报 `Hostname, IP, AgentVersion, PluginVersion`，把这四个记录组合成 `model.AgentReportRequest{}` 后调用 `g.HbsClient.Call("Agent.ReportStatus", req, &resp)` 向 Hbs 发送 rpc 上报



### 4.2 插件同步

1. `cron.SyncMinePlugins()` 同步插件，根据配置设置的间隔时间，执行 `g.HbsClient.Call("Agent.MinePlugins", req, &resp)` ，向 Hbs 发送 rpc 请求调用 `/hbs/rpc/agent.go` 中的 `MinePlugins()` 方法获取 plugin 列表  

2. 根据返回的 plugin 列表删除无用的 plugin 并增加新的 plugin 

   ```go
   desiredAll := make(map[string]*plugins.Plugin)
   for _, p := range pluginDirs {
   	underOneDir := plugins.ListPlugins(strings.Trim(p, "/"))
   	for k, v := range underOneDir {
   		desiredAll[k] = v
   	}
   }
   
   plugins.DelNoUsePlugins(desiredAll)
   plugins.AddNewPlugins(desiredAll)
   ```

3. 在 `main.go` 中 `import "falcon-plus/modules/agent/http"` ，http 包含有 init() 函数，该函数包含了 `configPluginRoutes()`，会根据文件是否存在执行 `git pull` 或者 `git clone`，git 操作的地址也就是在 `cfg.json` 中配置的 plugin git 地址



### 4.3 获取需要监听的端口/进程/url/路径

`cron.SyncBuiltinMetrics()` 为入口函数，根据配置设置的间隔时间定时调用 `g.SetReportUrls(urls), g.SetReportPorts(ports), g.SetReportProcs(procs), g.SetDuPaths(paths)` 

值得注意的是这里会与 Hbs 利用 md5 做 checksum 来减少网络开销



### 4.4 IP 白名单下发

`cron.SyncTrustableIps()`  根据配置定时向 Hbs 发起 rpc 请求，调用 `/hbs/rpc/agent.go` 中的 `TrustableIps()` 方法，获取白名单