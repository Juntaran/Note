# tcpdump

*2017.6.18*

## 1. tcpdump 选项与参数

    tcpdump [选项] [-c 数量]  [-F 表达式文件名] [-i 网卡名] [-r 读入文件名] [-s 抓包大小] [-T 解释类型] [-w 写入文件名 [-C 文件大小 [-W 文件数量]] [-U]] [表达式]
    
    
| 选项  | 参数  | 说明  | 重要  |
|---|---|---|---|
| **-A**  |   | 以 `ASCII 码`方式显示每一个数据包（不会显示数据包中链路层头部信息），在抓取包含网页数据的数据包时, 可方便查看数据  | √  |
| **-c**  | count  | 在接受到`count`个数据包后退出  | √  |
| **-C**  | file-size  | 该选项使得 tcpdump 在把原始数据包直接保存到文件中之前, 检查此文件大小是否超过`file-size`。如果超过了，将关闭当前文件，开启一个文件继续用于原始数据包的记录。file-size 的单位是百万字节（这里指1,000,000个字节，并非1024 ＊ 1024个字节）  | √  |
| -d  |   | 以容易阅读的形式打印，打印后退出  |   |
| -dd  |   | 以C语言的形式打印出包匹配码，打印后退出  |   |
| -ddd  |   | 以十进制数的形式打印出包匹配码，打印后退出  |   |
| **-D**  |   | 打印出系统中所有可以用 tcpdump 截包的网络接口，网络接口名字和数字编号可以用在 tcpdump 的`-i flag`  | √  |
| **-e**  |   | 在输出行打印出`数据链路层`的头部信息  | √  |
| -E  | spi@ipaddr algo:secret,...  | 解密IPsec ESP包  |   |
| **-f**  |   | 显示外部的 IPv4 地址时，采用数字方式而不是名字  | √  |
| -F  | file  | 使用`file`文件作为过滤条件表达式的输入，此时命令行上的输入将被忽略  |   |
| **-i**  | interface  | 指定`interface`为 tcpdump 需要监听的网络接口  | √  |
| -l  |   | 对标准输出进行行缓冲，遇到一个换行符就马上把这行的内容打印出来  |   |
| -L  |   | 列出指定网络接口所支持的数据链路层的类型后退出  |   |
| -m  | module  | 通过`module`指定的 file 装载 SMI、MIB 模块，用于 SNMP 协议数据包抓取  |   |
| -M  | secret  | 如果 TCP 数据包(TCP segments)有TCP-MD5选项，为其摘要的验证指定一个公共的密钥`secret`，RFC 2385  |   |
| **-n**  |   | 不把网络地址转换成名字  | √  |
| **-nn**  |   | 不进行端口名称的转换  | √  |
| -N  |   | 不打印出 host 的域名部分，`nic`而不是 `nic.ddn.mil`  |   |
| -O  |   | 不启用进行包匹配时所用的优化代码  |   |
| -p  |   | 一般情况下，把网络接口设置为`非混杂`模式.  |   |
| -q  |   | 静默输出，信息很少  |   |
| -R  |   | 对 ESP/AH 数据包的解析按照 RFC1825 而不是 RFC1829  |   |
| **-r**  | file  | 从文件`file`中读取包数据，如果`file`字段为`-`符号, 则 tcpdump 会从标准输入中读取包数据  | √  |
| -S  |   | 打印 TCP 数据包的顺序号时，使用绝对的顺序号，而不是相对的顺序号  |   |
| **-s**  | snaplen  | 设置 tcpdump 的数据包抓取长度为`snaplen`，默认为68字节，加上`-s 0`后可以抓到完整的数据包  | √  |
| -T  | type  | 强制 tcpdump 按`type`指定的协议所描述的包结构来分析收到的数据包（包括aodv、cnfp、rtcp、tftp）  |   |
| -t  |   | 不打印时间戳  |   |
| -tt  |   | 不对每行输出的时间进行格式处理  |   |
| -ttt  |   | tcpdump 输出时，每两行打印之间会延迟一个段时间（以毫秒为单位）  |   |
| -tttt  |   | 在每行打印的时间戳之前添加日期的打印  |   |
| -u  |   | 打印出未加密的 NFS  |   |
| -U  |   | 使得当 tcpdump 在使用`-w`选项时，其文件写入与包的保存同步  |   |
| **-v**  |   | 当分析和打印的时候，产生详细的输出。 比如，包的生存时间，标识，总长度以及 IP 包的一些选项。这也会打开一些附加的包完整性检测，比如对IP或ICMP包头部的校验和  | √  |
| -vv  |   | 产生比`-v`更详细的输出。比如，NFS 回应包中的附加域将会被打印，SMB 数据包也会被完全解码  |   |
| -vvv  |   | 产生比`-vv`更详细的输出。比如，telent 时所使用的 SB，SE 选项将会被打印  |   |
| **-w**  | file  | 把包数据直接写入`file`文件而不进行分析和打印输出，可以配合`-r`  | √  |
| **-W**  | filecount  | 与`-C`选项配合使用，这将限制可打开的文件数目，并且当文件数据超过`filecount`的限制时，依次`循环替代之前的文件`  | √  |
| -x  |   | 当分析和打印时，tcpdump 会打印每个包的头部数据，同时会以`16进制`打印出每个包的数据（但不包括连接层的头部）  |   |
| -xx  |   | tcpdump 会打印每个包的头部数据，同时会以`16进制`打印出每个包的数据，其中包括数据链路层的头部  |   |
| **-X**  |   | tcpdump 会打印每个包的头部数据，同时会以`16进制`和`ASCII码`形式打印出每个包的数据（但不包括连接层的头部） | √  |
| **-XX**  |   | tcpdump 会打印每个包的头部数据，同时会以`16进制`和`ASCII码`形式打印出每个包的数据，其中包括数据链路层的头部  | √  |
| -y  | datalinktype  | 设置 tcpdump 只捕获数据`链路层协议`类型是`datalinktype`的数据包  |   |
| -Z  | user  | 使 tcpdump 放弃自己的超级权限，并把当前tcpdump的用户ID设置为`user`  |   |


## 2. tcpdump 表达式

### 2.1 类型

| 类型  | 含义  |
|---|---|
| host  | 主机  |
| net  | 网络  |
| port  | 端口号  |

### 2.2 传输方向

| 类型  | 含义  |
|---|---|
| src  | 源  |
| dst  | 目的  |
| 默认  | 双向  |

### 2.3 协议

| 协议  | 层  |
|---|---|
| ether  | 链路层  |
| fddi  | 链路层  |
| tr  | 链路层  |
| wlan  | 链路层  |
| ppp  | 链路层  |
| slip  | 链路层  |
| link  | 链路层  |
| ip  | 网络层  |
| ip6  | 网络层  |
| arp  | 网络层  |
| rarp  | 网络层  |
| icmp  | 网络层  |
| tcp  | 传输层  |
| udp  | 传输层  |

常用 `tcp`、`udp`、`ip`、`ip6`、`arp`、`icmp`

### 2.4 运算符

#### 2.4.1 逻辑运算符

| 逻辑  | 符号  | 优先级  |
|---|---|---|
| 否  | `!` 或 `not`  | 1  |
| 与  | `&&` 或 `and`  | 2  |
| 或  | `| |` 或 `or`  | 2  |

结合顺序`自左向右`

#### 2.4.2 比较运算符

共有6个： `>`、`<`、`>=`、`<=`、`=`、`!=`


### 2.5 关键字

gateway、broadcast、less、greater


## 3. 使用技巧

1.  截获主机210.27.48.1 和主机210.27.48.2 或210.27.48.3的通信
    
        tcpdump host 210.27.48.1 and \ (210.27.48.2 or 210.27.48.3 \)
    
2. 截获主机192.168.126.131发送的所有数据包
    
        tcpdump -i ens33 src host 192.168.126.131
    
3. 截获 TCP 会话的开始和结束的数据包
    
        tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net localnet'
    
4. 打印所有通过网关snup的ftp数据包，并且数据包的源或目的不是本地网络上的主机。(nt: localnet, 实际使用时要真正替换成本地网络的名字))
    
        tcpdump 'gateway snup and (port ftp or ftp-data)'
    
5. 打印所有源或目的端口是80，网络层协议为IPv4，并且含有数据，而不是SYN、FIN以及ACK-only等不含数据的数据包
    
        tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
    
6. 打印长度超过576字节，并且网关地址是 snup 的IP数据包
    
        tcpdump 'gateway snup and ip[2:2] > 576'
    
7. 打印所有IP层广播或多播的数据包，但不是物理以太网层的广播或多播数据报
    
        tcpdump 'ether[0] & 1 = 0 and ip[16] >= 224'
    
8. 打印所有非 ping 程序产生的数据包即打印除'echo request'或者'echo reply'类型以外的ICMP数据包
    
        tcpdump 'icmp[icmptype] != icmp-echo and icmp[icmptype] != icmp-echoreply'
    
9. 打印使用 ftp 端口和 ftp 数据端口的数据包
    
        tcpdump 'port ftp or ftp-data'
    
10. 截取HTTP数据包

0x4745->"GE"  
0x4854->"HT"  

        tcpdump  -XvvennSs 0 -i eth0 tcp[20:2]=0x4745 or tcp[20:2]=0x4854
        
______


## Reference:
* [tcpdump抓包命令详解](http://www.360doc.com/content/17/0618/16/14454117_664203330.shtml)
* [kofandlizi: tcpdump抓取HTTP包](http://blog.csdn.net/kofandlizi/article/details/8106841)
* [Linux tcpdump命令详解](http://www.cnblogs.com/ggjucheng/archive/2012/01/14/2322659.html)
* [Linux大棚](http://www.broadview.com.cn/book/122)
