# IPv6

2017年7月14日，IPv6 完成标准化，RFC 8200 诞生  
本篇可以近似视作 RFC 8200 的翻译

## 1 简介

从 [IPv4](https://tools.ietf.org/html/rfc791) 到 [IPv6](https://tools.ietf.org/html/rfc8200) 的变化主要体现在以下几个方面:

1. 更多的地址容量

    IPv6 把 IP 地址长度从 32bits 增加到了 128bits，大大增加了地址数量并且可以更简单地自动配置地址。组播路由的可伸缩性也又了提高，这得益于对组播地址增加了一个 `scope` 的字段。此外，IPv6 新定义了一个地址类型 `anycast address` (选播地址)，它被用来发送一个 `Packet` (数据包/分组)到一组节点

2. 简化头部格式

    一些 IPv4 头的字段被删除或者变成可选，从而减少数据包处理的时间并限制 IPv6 包头的带宽成本

3. 提升对扩展和选项的支持

    IP 头部选项的改变令其更有效地转发，长度不太严格的选项，以及在未来会引入新的选项来增强灵活性

4. 流量标签功能

    新增了一个允许发送端的请求数据包序列标记为单个流

5. 认证和隐私功能

    为 IPv6 增加了支持认证、数据完整性、(可选)数据机密性的特性扩展

IPv6 的规范和语义在 [RFC 4291](https://tools.ietf.org/html/rfc4291) 中规定，ICMP 的 IPv 版本，以及所有 IPv6 的实现在 [RFC 4443](https://tools.ietf.org/html/rfc4443) 中规定

## 2 术语

## 3 IPv6 头部格式

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

## 4 IPv6 扩展头

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

## 5 包大小

## 6 流标签 (Flow Labels)

## 7 通信量类 (Traffic Classes)

## 8 上层协议

## 9 国际互联网代理成员管理局-Internet Assigned Numbers Authority(IANA)

## 10 安全问题



- [RFC 8200](https://tools.ietf.org/html/rfc8200) 
- [RFC 8200 PDF](http://www.rfc-editor.org/rfc/pdfrfc/rfc8200.txt.pdf) 
- [RFC 2474 IPv4 与 IPv6 头差异](https://tools.ietf.org/html/rfc2474)
