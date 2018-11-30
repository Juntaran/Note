# Judge

Judge 用于告警判断，Agent 将数据 push 给 Transfer，Transfer 不但会转发给 Graph组件来绘图，还会转发给 Judge 用于判断是否触发告警



## 1 配置说明

```yaml
{
    "debug": true,
    "debugHost": "nil",
    "remain": 11,
    "http": {
        "enabled": true,
        "listen": "0.0.0.0:6081"
    },
    "rpc": {
        "enabled": true,
        "listen": "0.0.0.0:6080"
    },
    "hbs": {
        "servers": ["127.0.0.1:6030"], # hbs最好放到lvs vip后面，所以此处最好配置为vip:port
        "timeout": 300,
        "interval": 60
    },
    "alarm": {
        "enabled": true,
        "minInterval": 300, # 连续两个报警之间至少相隔的秒数，维持默认即可
        "queuePattern": "event:p%v",
        "redis": {
            "dsn": "127.0.0.1:6379", # 与alarm、sender使用一个redis
            "maxIdle": 5,
            "connTimeout": 5000,
            "readTimeout": 5000,
            "writeTimeout": 5000
        }
    }
}
```

