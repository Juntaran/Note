# iptables

*2017.6.16*

## 1.四表五链

iptables有`四表五链`一说，即  

### 1.1 四表：
> **filter**： 默认表，包含防火墙过滤的规则，内置规则链为INPUT、OUTPUT、FORWARD，内核模块对应 iptables_filter  
> **nat**： 用于 nat 功能（端口映射、地址映射等），包含源和目的地址及端口转发的规则，内置规则链为 PREROUTING、OUTPUT 和 POSTROUTING，内核模块对应 iptables_nat  
> **mangle**：用于对特定的数据包修改，设置特殊的数据包路由标志的规则，这些标志随后被 Filter 表中的规则检查，内置规则链为 PREROUTING、INPUT、FORWARD、POSTROUTING 和 OUTPUT，内核模块对应  iptable_mangle  
> **raw**： 优先级最高，设置 Raw 时一般是为了不再让 iptables 做数据包的链接跟踪处理，提高性能，内置规则链为 OUTPUT 和  PREROUTING，内核模块对应 iptable_raw  

### 1.2 五链：
> **INPUT**： 当一个数据包由内核的路由计算确定为本地的 Linux 系统后，它会通过 INPUT 链的检查——进来的数据包应用此规则链中的策略  
> **OUTPUT**： 保留给系统自身生成数据包——外出的数据包应用此规则链中的策略  
> **FORWARD**： 经过 Linux 系统路由的数据包——转发数据包时应用此规则链中的策略  
> **PREROUTING**： 用于修改目标地址（DNAT），数据包在进入系统之前——对数据包作路由选择前应用此链中的规则（所有的数据包进来的时侯都先由这个链处理）  
> **POSTROUTING**： 用于修改源地址（SNAT），发送到网卡接口之前——对数据包作路由选择后应用此链中的规则（所有的数据包出来的时侯都先由这个链处理）  

### 1.3 规则表之间的优先级顺序

raw > mangle > nat > filter


## 2. 数据包的流向

### 2.1 常见的两种流向

    PREROUTING -> FORWARD -> POSTROUTING
    
    PREROUTING -> INPUT -> 本机 OUTPUT -> POSTROUTING
    
这两种流向分别对应了`iptables`的两种工作模式：`NAT 路由器`和`主机防火墙`


### 2.2 流向三种情况

#### 第一种情况：入站数据流向

从外界到达防火墙的数据包，先被`PREROUTING规则链`处理（是否修改数据包地址等），之后会进行路由选择（判断该数据包应该发往何处），如果数据包的目标主机是防火墙本机（比如说 Internet 用户访问防火墙主机中的 web 服务器的数据包），那么内核将其传给`INPUT链`进行处理（决定是否允许通过等），通过以后再交给系统上层的应用程序（比如 Apache 服务器）进行响应。

#### 第二种情况：转发数据流向

来自外界的数据包到达防火墙后，首先被`PREROUTING规则链`处理，之后会进行路由选择，如果数据包的目标地址是其它外部地址（比如局域网用户通过网关访问 QQ 站点的数据包），则内核将其传递给`FORWARD链`进行处理（是否转发或拦截），然后再交给`POSTROUTING规则链`（是否修改数据包的地址等）进行处理。

#### 第三种情况：出站数据流向

 防火墙本机向外部地址发送的数据包（比如在防火墙主机中测试公网 DNS 服务器时），首先被`OUTPUT规则链`处理，之后进行路由选择，然后传递给`POSTROUTING规则链`（是否修改数据包的地址等）进行处理。
 
 
 ## 3. iptables 规则设置
 
 整体语法：
 
     iptables [-t 表名] <-A | I | D | R > 链名 [规则编号] [-i | o 网卡名称] [-p 协议类型] [-s 源IP地址 | 源子网] [--sport 源端口号] [-d 目的IP地址 | 目标子网] [--dport 目的端口号] <-j 动作>
     
### 3.1 定义默认策略

    iptables [-t 表名] <-P> <链名> <动作>
    
### 3.2 查看 iptables 规则

    iptables [-t 表名] -(nv)L [链名] (--line-number)

| 参数 | 说明 |
| --- | --- |
| -L | 查看当前表的所有规则，默认查看的是filter表，如果要查看NAT表，可以加上-t NAT参数 |
| -n | 不对ip地址进行反查，加上这个参数显示速度会快很多 |
| -v | 输出详细信息，包含通过该规则的数据包数量，总字节数及相应的网络接口 |
| –line-number | 显示规则的序列号，这个参数在删除或修改规则时会用到 |

### 3.3 增、删、改、替换 iptables 规则

     iptables [-t 表名] <-A | I | D | R > 链名 [规则编号] [-i | o 网卡名称] [-p 协议类型] [-s 源IP地址 | 源子网] [--sport 源端口号] [-d 目的IP地址 | 目标子网] [--dport 目的端口号] <-j 动作>
 
| 参数 | 说明 |
| --- | --- |
| -t | 指定表，默认 filter |
| -A | ADD 增加一条规则，增加到最后一行，该参数**不能指定**规则编号 |
| -I | INSERT 插入一条规则，如果没有指定规则编号，则插入成为第一条 |
| –D | DELETE 删除一条规则，可以直接指定规则号，也可以输入完整规则 |
| –R | REPLACE 替换一条规则，**必须指定**被替换的规则号 |
| –i | 指定数据包从哪个网卡流入 |
| –o | 指定数据包从哪个网卡流出 |

| 动作  | 说明  |
|---|---|
| ACCEPT  | 接收数据包  |
| DROP  | 丢弃数据包  |
| REDIRECT  | 重定向数据包到本机或另外某台机器的某个端口，通常用来实现透明代理或对外开放内网的服务  |
| REJECT  | 拦截该数据包，并发送封包通知对方  |
| SNAT  | 改变数据包的源地址，在 NAT 表的 POSTROUTING 链上进行该动作  |
| DNAT  | 改变数据包的目的地址，在 NAT 表的 PREROUTING 链上进行该动作  |
| MASQUERADE  | IP 伪装，即 NAT 技术，MASQUERADE 只能用于 ADSL 等拨号上网的 IP 伪装，也就是主机 IP 必须为 ISP 动态分配，静态分配需要使用 SNAT  |
| LOG  | 日志功能，将符合规则的数据包相关信息记录在日志里  |

### 3.4 清楚规则和计数器

    iptables [-t 表名] <-F | X | Z>
    
| 参数 | 说明 |
| --- | --- |
| -t | 指定表，默认 filter |
| -F | 删除指定表里所有规则 |
| -X | 删除用户自定义的空链 |
| -Z | 将指定表的数据包计数器和流量计数器清零 |

## 4. iptables 的状态

### 4.1 iptables 数据包的四种状态

| 状态  | 说明  |
|---|---|
| NEW  | 主机向远程主机发送一个连接请求，该数据包状态为 NEW  |
| ESTABLISHED  | 三次握手后，主机和远程主机通信数据的状态为 ESTABLISH  |
| RELATED  | 如果出现了 RELATED 状态，那么一定已经有一个 ESTABLISH 与其相关，例如 FTP 服务：21端口传输命令，20端口传输数据，21端口状态为 ESTABLISH，20端口则为 RELATED  |
| INVALID  | 无效的数据包，不能识别属于哪个连接或没有任何状态，通常这种数据包会被丢弃  |

### 4.2 针对状态的命令

    iptables -m state --state [NEW | ESTABLISHED | RELATED | INVALID]
    
可以将 -m 之后的内容与 `3.3` 的规则结合

### 5. iptables 的记录

#### 5.1 Conntrack 记录

不建议在生产服务器开启`conntrack`功能，及消耗内存  
可以通过`/proc/sys/net/ipv4/ip_conntrack_max`里进行查看和设置  
查看`conntrack`记录

    cat /proc/net/ip_conntrack
    
#### 5.2 iptables 默认规则

    cat /etc/sysconfig/iptables
    
### 6. iptables 规则的保存与恢复

    //将规则保存在/etc/sysconfig/iptables文件里
    service iptables save
    
    //重启Iptables服务
    service iptables restart
    

### 7. 其他

快速检测和防御`SYN flood`攻击

    echo "1" > /proc/sys/net/ipv4/tcp_syncookies
    
iptables 作为 NAT 路由器时，存在多网卡现象，需要开启`IP 转发功能`，用于多个网卡之间数据流通

    echo "1" > /proc/sys/net/ipv4/ip_forward

______


## Reference:
* [Linuxeye: iptables里的四表五链](http://www.linuxeye.com/security/1035.html)
* [Linux公社: SNAT、DNAT——iptables防火墙基础策略汇总](http://www.linuxidc.com/Linux/2013-08/88536.htm)
* [AshlingR: 通过iptables实现数据包转发](http://blog.csdn.net/ashlingr/article/details/8947444)
* [构建高可用Linux服务器](http://www.hzbook.com/Books/8030.html)
