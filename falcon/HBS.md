# HBS

## 1 职责

1.1 处理 agent 心跳请求，填充 host 表

​	策略配置 web 端(Portal 模块)，存在 group 概念，对机器进行了分组，portal 数据库中有一个 host 表，存放了机器信息(hostname、ip、agent 版本、插件版本)。agent 每分钟调用一次 hbs rpc 接口发送一个心跳包，发送一些信息（agent版本、插件版本）给 hbs，hbs 写入数据库

1.2 将 ip 白名单分发到所有 agent

​	agent 存在一个 http 的 run 接口，可以接受发送过来的 shell 指令在本机执行，比较危险，所以增加了白名单，只有在白名单里的机器发送的指令才会被执行（hbs 配置中的 trustable ips）, agent 每分钟调用一下 hbs rpc 接口获取授信的 IP 列表 

1.3 告诉各个 agent 需要执行哪些插件

​	agent  采集信息可能不够用，所以允许用户编写采集脚本，对 agent 功能进行扩展。agent 配置中含有了 get repo 地址，调用 agent http 接口 -> plugin update 接口可以出发 agent 主动去 `git pull` ，这就意味所有的机器都 clone 了所有脚本。哪些 agent 需要执行哪些插件，这个信息是在 portal 中进行配置的，通过 hbs 分发给 agent

1.4 告诉各个 agent 需要监听哪些端口、进程

​	