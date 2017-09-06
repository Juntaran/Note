# Nginx+https+iOS

*2017.9.5*

最近在公司遇到了一个神奇的问题：  
nginx 配置的 https 域名，windows 和 android 可以正常登陆  
iOS 无论是 mac 还是 iphone ，不管是 safrai 、 chrome 还是 UC  
都不能访问  

___

## 抓包分析：  

![Problem](https://raw.githubusercontent.com/Juntaran/Note/master/pictures/nginx%2Bhttps%2Bios.jpg)

可以看到从第240行，开始 TLS 握手  
第256行，手机向服务器发送了一个 `Application Data`  
第257行，服务器返回了一个 ACK  

第258行，神奇的事情发生了，手机再次向服务器发送了一个 `Application Data`  
可以看到这个数据包和第256行一模一样，被 wireshark 标记为了 `TCP Spurious Retransmission` ，即虚假重传  
第259行，服务器懵逼了，发送一个 RST 来复位，标记本连接异常要把它关掉  

第287行，又开始循环，客户端向服务器发起 TLS 握手  
按照上述循环，在第312行，又开始了 `TCP Spurious Retransmission`   

依此反复，直到彻底断开  


## 解决方案：  

和同事试了一下午，终于解决了= =  
一开始我们把 ssl 配置部分全部粘贴了一遍，发现可以运行  

之后被好奇心的驱使，一行一行地试，终于发现  

在 nginx 的配置文件的 ssl 配置处，  增加一行  

```
ssl_session_cache shared:SSL:10m;
```

就解决问题了  


什么？  
你问我这句话有什么用？  
我 TM 也不知道啊，Google 了一下 `ssl_session_cache ios`  

相关的问题很少，有那么一两个老外兄弟也碰到了这个诡异的情况  
也是通过一条条用手试，试出来的  

such as:  
* [Apple Safari browsers fail to connect](https://community.letsencrypt.org/t/apple-safari-browsers-fail-to-connect/3731)


在我看来， iOS 的脑回路就是有坑，  
ssl_session_cache 的本意是设置一个 cache  
通过重用 Session 来提高 https 性能  

为什么这句话能解决这个问题呢？  
iOS 重发第二个 `Application Data` 因为服务器之前已经有缓存了所以不会接收  
因此服务器不会认为连接异常，避免了 RST 复位  


## TLS 握手过程：  

| Client  | Server  |
|---|---|
| Client Hello  |   |
|   | Server Hello  |
|   | Certificate  |
|   | (Server Key Exchange)  |
|   | (certificate_request)  |
|   | Server Hello Done  |
| (Certificate)  |   |
| Client Key Exchange  |   |
| (certifiate_verify)  |   |
| Change Cypher Spec  |   |
|   | Change Cyper Spec  |

在 `Client Hello` 中，客户端会通知服务器自己支持的加密类型  

```
Cipher Suites (19 suites)
    Cipher Suite: TLS_EMPTY_RENEGOTIATION_INFO_SCSV (0x00ff)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384 (0xc02c)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256 (0xc02b)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 (0xc024)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256 (0xc023)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA (0xc00a)
    Cipher Suite: TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA (0xc009)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (0xc030)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (0xc02f)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (0xc028)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (0xc027)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (0xc014)
    Cipher Suite: TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (0xc013)
    Cipher Suite: TLS_RSA_WITH_AES_256_GCM_SHA384 (0x009d)
    Cipher Suite: TLS_RSA_WITH_AES_128_GCM_SHA256 (0x009c)
    Cipher Suite: TLS_RSA_WITH_AES_256_CBC_SHA256 (0x003d)
    Cipher Suite: TLS_RSA_WITH_AES_128_CBC_SHA256 (0x003c)
    Cipher Suite: TLS_RSA_WITH_AES_256_CBC_SHA (0x0035)
    Cipher Suite: TLS_RSA_WITH_AES_128_CBC_SHA (0x002f)
```

在 `Server Hello` 中，服务器会选取一个告知 Client  

```
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (0xc030)
```

## iOS 的 ATS：

ATS: App Transport Security  

必须是苹果信任的CA证书机构颁发的证书
iOS 后台传输协议必须满足: TLS1.2   
签字算法只能是下面的一种:  
```
  TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
  TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
  TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384
  TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA
  TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256
  TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA
  TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
  TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
  TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
  TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256
  TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA
```

这意味着 Apache ，Nginx 要求关联的 openssl 版本在 1.0.1+ ，这样网站才支持 TLS1.2   
同时您需要对证书相关参数做一定调整：

```
Apache:  

  SSLProtocol all -SSLv2 -SSLv3
  SSLCipherSuite ECDH:AESGCM:HIGH:!RC4:!DH:!MD5:!aNULL:!eNULL;
```

```
Nginx:  

  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
  ssl_ciphers ECDH:AESGCM:HIGH:!RC4:!DH:!MD5:!aNULL:!eNULL;
```
___
## Reference:  

* [iOS 升级 HTTPS 通过 ATS 你所要知道的](http://ios.jobbole.com/91645/)
* [HTTPS 背后的加密算法](http://insights.thoughtworkers.org/cipher-behind-https/)
* [服务器配置 ssl 证书支持苹果 ATS 方法](http://www.cnblogs.com/kabi/p/6198064.html)
* [NGinx and htpasswd](https://trac.nginx.org/nginx/ticket/235)