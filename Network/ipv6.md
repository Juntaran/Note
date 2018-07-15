# IPv6

2017年7月14日，IPv6 完成标准化，RFC 8200 诞生  
本篇可以近似视作 RFC 8200 的翻译

****
## 目录

* [1 简介](#1-简介)
* [2 术语](#2-术语)
* [3 IPv6 头部格式](#3-头部格式)
* [4 IPv6 扩展头](#4-扩展头)
    * [4.1](#4.1)
    * [4.2](#4.2)
    * [4.3](#4.3)
    * [4.4](#4.4)
    * [4.5](#4.5)
    * [4.6](#4.6)
    * [4.7](#4.7)
    * [4.8](#4.8)
* [5 数据包大小](#5-数据包大小)
* [6 流标签](#6-流标签) 
* [7 通信量类](#7-通信量类)
* [8 上层协议](#8-上层协议)
    * [8.1](#8.1)
    * [8.2](#8.2)
    * [8.3](#8.3)
    * [8.4](#8.4)
* [9 IANA 建议](#9-IANA) 
* [10 安全问题](#10-安全问题)
___

## 1 简介

从 [IPv4](https://tools.ietf.org/html/rfc791) 到 [IPv6](https://tools.ietf.org/html/rfc8200) 的变化主要体现在以下几个方面:

1. 更多的地址容量

    IPv6 把 IP 地址长度从 32bits 增加到了 128bits，大大增加了地址数量并且可以更简单地自动配置地址。组播路由的可伸缩性也又了提高，这得益于对组播地址增加了一个 `scope` 的字段。此外，IPv6 新定义了一个地址类型 `anycast address` (选播地址)，它被用来发送一个 `Packet` (数据包/分组)到一组节点

2. 简化头部格式

    一些 IPv4 头的字段被删除或者变成可选，从而减少数据包处理的时间并限制 IPv6 包头的带宽成本

3. 提升对扩展和选项的支持

    IP 头部选项的改变令其更有效地转发，长度不太严格的选项，以及在未来会引入新的选项来增强灵活性

4. 流量标签功能

    新增了一个允许发送端的请求数据包序列标记为单个流

5. 认证和隐私功能

    为 IPv6 增加了支持认证、数据完整性、(可选)数据机密性的特性扩展

IPv6 的规范和语义在 [RFC 4291](https://tools.ietf.org/html/rfc4291) 中规定，ICMP 的 IPv 版本，以及所有 IPv6 的实现都在 [RFC 4443](https://tools.ietf.org/html/rfc4443) 中规定  
IPv6 的数据传输与 IPv4 相同，可以查看 [RFC 791](https://tools.ietf.org/html/rfc791) 的附录B

## 2 术语

|  名称  |  意义  |
|----|----|
|  node  |  实现了 IPv6 的设备  |
|  router  |  一个转发 IPv6 数据包但是地址不是自己的设备  |
|  host  |  除了 router 的任何 node  |
|  upper layer  |  基于 IPv6 实现的协议层  |
|  link  |  一种通信设备或媒介，node 它可以在链路层通信，比如以太网（简单/桥接）；PPP 链路；X.25，帧中继，ATM 网络；以及互联网层或更高层的隧道，比如 IPv4 或 IPv6 本身的隧道  |
|  neighbors  |  连接到同一链路的节点  |
|  interface  |  节点依赖它连接到链路  |
|  address  | 一个 interface 或一组 interface 的 IPv6 层标识符   |
|  packet  |  IPv6 头 + 载荷  |
|  link MTU  |  最大传输单元  |
|  path MTU  |  源 node 和目的 node 间所有链路中的最小链路 MTU  |

> 注意：
> 对于一个具有多个网卡的设备，是可以配置成从它的一部分网卡（非所有）转发非自身到达的数据包并丢弃从其他网卡接收到的非自身到达的数据包  
> 前置网卡也就是发送端必须服从路由器的发送数据包、与 neighbors 交互的协议要求
> 后置网卡也就是接收端必须满足对于 hosts(主机)的接收数据包、与 neighbors 交互的协议要求

## 3 头部格式

```
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |Version| Traffic Class |              Flow Label               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |         Payload Length        |  Next Header  |   Hop Limit   |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 +                                                               +
 |                                                               |
 +                        Source Address                         +
 |                                                               |
 +                                                               +
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                                                               |
 +                                                               +
 |                                                               |
 +                      Destination Address                      +
 |                                                               |
 +                                                               +
 |                                                               |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```


 |  名称  |  作用  |
|----|----|
|  Version  |  4-bit 协议版本值为 6  |
|  Traffic Class  |  8-bit [通信量类](#7-通信量类)  |
|  Flow Label  |  20-bit [流标签](#6-流标签)  |
|  Payload Length  |  16-bit 无符号整型，IPv6 有效载荷的长度，即该 IPv6 报头后面的分组的剩余部分，单位为 8-bit(Bytes)，注意[任何扩展标头](#4-扩展头)都被认为是有效载荷的一部分，也就是说扩展头包括在长度计数中  |
|  Next Header  |  8-bit 选择器，表示跟在 IPv6 头后面的类型，用途相当于 IPv4 头部的[协议号](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)  |
|  Hop Limit  |  8-bit 无符号整型。通过转发数据包的每个节点递减 1。当转发时，如果接收到跳数为零或被递减到零，则丢弃该分组。作为分组目的地的节点不应该丢弃跳数等于零的分组；它应该正常处理分组  |
|  Source Address  |  128-bit，数据包发送者的地址，可以参考 [RFC 4291](https://tools.ietf.org/html/rfc4291)   |
|  Destination Address  |  128-bit，数据包接收者的地址（如果存在路由头部，可能不是最终接收者），可以参考 [RFC 4291](https://tools.ietf.org/html/rfc4291) 和 [4.1 节](#4.1)  |



## 4 扩展头

IPv6 的扩展头代替了 IPv4 头的可选项，在一个数据包中，IPv6 的可选网络层信息是夹在 IPv6 头和上层协议头中间的  
有少量的扩展头每个都由 `Next Header` 值标记  

扩展头根据 [IP 协议号](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml)编号，IPv4 和 IPv6 使用相同的值  
当处理数据包中一系列的 `Next Header` 值时，第一个不是扩展头，[IANA-EH](https://www.iana.org/assignments/ipv6-parameters/ipv6-parameters.xhtml) 中表明这是下一个才是上层头部的对应值  
当没有上层头部时，使用一个特殊的 `No Next Header` 值  

一个 IPv6 数据包可以携带任意个扩展头，每个扩展头由前一个报头的 `Next Header` 定义


```
+---------------+------------------------
|  IPv6 header  | TCP header + data
|               |
| Next Header = |
|      TCP      |
+---------------+------------------------
+---------------+----------------+------------------------
|  IPv6 header  | Routing header | TCP header + data
|               |                |
| Next Header = | Next Header =  |
|    Routing    |      TCP       |
+---------------+----------------+------------------------
+---------------+----------------+-----------------+-----------------
|  IPv6 header  | Routing header | Fragment header | fragment of TCP
|               |                |                 | header + data
| Next Header = | Next Header =  |  Next Header =  |
|    Routing    |    Fragment    |       TCP       |
+---------------+----------------+-----------------+-----------------
```

扩展头（除了 `Hop-by-Hop` 可选头）不会被任何沿着数据包传输路径的节点处理、增加或者删除，直到数据包到达 IPv6 头中 `Destination Address` 定义的节点（或是多播节点中的任意节点） 
`Hop-by-Hop` 选项头不会被增加或删除，但是可能会被数据包沿途经过的任何节点处理或校验，直到数据包到达 IPv6 头中 `Destination Address` 定义的节点（或是多播节点中的任意节点）  
`Hop-by-Hop` 可选头当出现时，必须紧跟 IPv6 头，它的存在由 IPv6 头中的 `Next Header` 处的 `0` 值表示

> 注意:  
> 虽然 [RFC-2460](https://tools.ietf.org/html/rfc2460) 中要求所有节点必须检查并处理 `Hop-by-Hop` 可选头，但是现在是否处理 `Hop-by-Hop` 可选头，只会在配置中明确表示要处理才会处理




## 5 数据包大小

## 6 流标签

Flow Labels


## 7 通信量类

Traffic Classes

## 8 上层协议

## 9 IANA

国际互联网代理成员管理局-Internet Assigned Numbers Authority(IANA)

## 10 安全问题



- [RFC 8200](https://tools.ietf.org/html/rfc8200) 
- [RFC 8200 PDF](http://www.rfc-editor.org/rfc/pdfrfc/rfc8200.txt.pdf) 
- [RFC 2474 IPv4 与 IPv6 头差异](https://tools.ietf.org/html/rfc2474)
