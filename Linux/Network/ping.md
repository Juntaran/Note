# ping

*2017.6.20*

    ping  [-aAbBdDfhLnOqrRUvV46] [-c count] [-F flowlabel] [-i interval] [-I interface] [-l preload] [-m mark] [-M pmtudisc_option] [-N nodeinfo_option] [-w deadline] [-W timeout] [-p pattern] [-Q tos] [-s packetsize] [-S sndbuf] [-t ttl] [-T timestamp option] [hop ...] destination

重点参数列表：

| 参数  | 说明  |
|---|---|
| -4  | 使用IPv4  |
| -6  | 使用IPv6  |
| -b  | ping一个广播地址  |
| -c count  | 指定 ping 的次数为`count` |
| -D  | 打印时间戳  |
| -f  | flood ping，必须有 root 权限 |
| -i interval  | 每隔`interval`秒 ping 一次  |
| -I interface  | 使用指定的`interface`网卡 ping  |
| -l preload  | 在发送前`preload`个数据包的时候不等待 reply，preload > 3 需要 root权限  |
| -n  | 使用数字输出，不尝试转换为 host   |
| -p pattern | 指定用16个“填充”字节`pattern`填充发送的包，`-p ff` 则为全部用1填充  |
| -q  | 不显示任何传送封包的信息，只显示最后的结果  |
| -s packetsize | 指定 ping 的数据包大小，默认64字节  |
| -t ttl  | 指定 ping 的 TTL 为`ttl`，路由器转发数据包时，TTL 值会减一，为0则该数据包生命终止  |
| -w deadline  | 设定终止时间为`deadline`，应与`-c count`配合使用  |
| -W timeout  | 设定等待回应的时间为`timeout`  |