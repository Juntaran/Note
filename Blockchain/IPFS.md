# IPFS

## 1 简介

IPFS(InterPlanetary File System)，星际文件系统  
名字很好听，是一个 `点对点的分布式版本文件系统` ，目标是为了补充(取代) HTTP  
把所有具有 `相同文件` 系统的计算设备连接在一起  
用 `基于内容` 的地址替代`基于域名`的地址  
这样用户寻找的不是某个 `地址` 而是存储在某个地方的 `内容`   
无需验证发送者的身份，只验证内容的 hash 值  
从而提升网页速度、更快、更安全  

可以把 IPFS 想象成所有文件数据是在同一个 BitTorrent 群并且通过同一个 Git 仓库存取  

## 2 IPFS 原理

HTTP 可以视为一种集中化的协议，有以下几个缺点:  

1. 容易遭受 DDoS 攻击  
2. 过度依赖于骨干网  
3. 容易被监视审查控制  

HTTP 首先 `基于域名` 寻找服务器 IP 地址，之后根据路径访问资源  
IPFS 则是根据内容哈希，通过底层的 DHT(分布式哈希表) 来快速找到拥有数据的节点  
可以把 IPFS 简单视作为 CDN  

以下摘自 http://www.infoq.com/cn/articles/ipfs  

> 向 IPFS 分布式网络询问哈希的时候，它通过使用一个分布式哈希表  
> 可以快速（在一个拥有 10,000,000 个节点的网络中只需要 20 跳）地找到拥有数据的节点  
> 从而检索该数据，并使用哈希验证这是否是正确的数据  
> 
> IPFS 是通用的，并且存储限制很少。它服务的文件可大可小  
> 对于一些大的文件，它会自动将其切割为一些小块，使 IPFS 节点不仅仅可以像 > > HTTP 一样从一台服务器上下载文件，而且可以从数百台服务器上进行同步下载  
> IPFS 网络是一个细粒度的、不可靠的、分布式的、易联合的内容分发网络（Content Delivery Network , CDN）  
> 对于所有数据类型都是很有用的，包括图像、视频流、分布式数据库、操作系统、blockchains 等，而对于 IPFS 来说，最重要的是静态 web 网站  
> 
> IPFS 文件也可以是特殊的 IPFS 目录对象，它允许用户使用人类可读的文件名，透明地链接到其他 IPFS 哈希  
> 用户可以通过默认方式加载目录中的 index.html，这也是标准的 HTTP 服务器采用的方式  
> 使用目录对象，IPFS可允许用户采用完全相同的方式生成静态网站  
> 将 web 网站添加到 IPFS 节点中只需要 `ipfs add -r yoursitedirectory`  
> 在此之后，用户可以从任何 IPFS 节点访问，而不需要链接到 HTML 上的任何哈希  

简而言之就是结合 DHT 和 blockchain 组成了一个 "CDN"  

## 3 使用前提

- 自备翻墙 :L  
- Mac | Linux (虽然 Windows 也支持，但是我并不想研究)  
- Go Env (最好有，如果喜欢源码编译的话)

## 4 安装 GPG

``` bash
brew install gnupg

gpg --gen-key


# 输入相关信息，结果如下:  

# 我们需要生成大量的随机字节。这个时候您可以多做些琐事(像是敲打键盘、移动
# 鼠标、读写硬盘之类的)，这会让随机数字发生器有更好的机会获得足够的熵数。
# 我们需要生成大量的随机字节。这个时候您可以多做些琐事(像是敲打键盘、移动
# 鼠标、读写硬盘之类的)，这会让随机数字发生器有更好的机会获得足够的熵数。
# gpg: /Users/juntaran/.gnupg/trustdb.gpg：建立了信任度数据库
# gpg: 密钥 1ED9DF99E4F3A740 被标记为绝对信任
# gpg: directory '/Users/juntaran/.gnupg/openpgp-revocs.d' created
# gpg: revocation certificate stored as '/Users/juntaran/.gnupg/openpgp-revocs.d/07B03EDCEE49F5AFF4CE0C121ED9DF99E4F3A740.rev'
# 公钥和私钥已经生成并经签名。

# pub   rsa2048 2018-03-12 [SC] [有效至：2020-03-11]
#       07B03EDCEE49F5AFF4CE0C121ED9DF99E4F3A740
# uid                      Juntaran <jacinthmail@gmail.com>
# sub   rsa2048 2018-03-12 [E] [有效至：2020-03-11]
```

``` bash
# 导出公钥
gpg --export --armor jacinthmail@gmail.com > Juntaran.pub.asc

# 导出私钥
gpg -o Juntaran.sec.key --export-secret-keys Juntaran
```

可以使用以下命令导入你生成的 pubkey:  

```
gpg --import pubkey.asc
```

列出 key:   

```
gpg --list-keys
```

## 5 安装 IPFS

参考 https://ipfs.io/docs/install/ 安装  

``` bash
# 源码编译(我建议还是算了)
go get github.com/jbenet/go-ipfs/cmd/ipfs

# Linux
wget https://dist.ipfs.io/go-ipfs/v0.4.13/go-ipfs_v0.4.13_linux-amd64.tar.gz

# Mac OS
wget https://dist.ipfs.io/go-ipfs/v0.4.13/go-ipfs_v0.4.13_darwin-amd64.tar.gz

tar xfz go-ipfs_v0.4.13_darwin-amd64.tar.gz
cd go-ipfs 
./install.sh

# Test
ipfs help
```

初始化:  

``` sh
ipfs init

# 结果

initializing IPFS node at /Users/juntaran/.ipfs
generating 2048-bit RSA keypair...done
peer identity: QmdA8cVQeFEjTBFNvLQXzsJtYDCjD3HacaSjTCLVhN2Md1
to get started, enter:

	ipfs cat /ipfs/QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/readme


# 节点数据同步
ipfs daemon

# 结果

# Initializing daemon...
# Swarm listening on /ip4/10.232.64.161/tcp/4001
# Swarm listening on /ip4/10.37.129.2/tcp/4001
# Swarm listening on /ip4/127.0.0.1/tcp/4001
# Swarm listening on /ip6/::1/tcp/4001
# Swarm listening on /p2p-circuit/ipfs/QmdA8cVQeFEjTBFNvLQXzsJtYDCjD3HacaSjTCLVhN2Md1
# Swarm announcing /ip4/10.232.64.161/tcp/4001
# Swarm announcing /ip4/10.37.129.2/tcp/4001
# Swarm announcing /ip4/127.0.0.1/tcp/4001
# Swarm announcing /ip6/::1/tcp/4001
# API server listening on /ip4/127.0.0.1/tcp/5001
# Gateway (readonly) server listening on /ip4/127.0.0.1/tcp/8080
# Daemon is ready    
```

随便找一个文件放到 `ipfs` 的目录里  

``` bash
gpg --encrypt --recipient "Juntaran" test.pdf

# md5检验
md5sum test.pdf
# 57f4e4fd59c28ea46a759e5886ef9df3  test.pdf
```

此时该文本已经被加密  
上传到 ipfs

``` sh
ipfs add test.pdf.gpg

# 结果
# added QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr test.pdf.gpg

# 如果想上传一个目录 -r

# 检查是否上传成功
ipfs pin ls | grep QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr

# 结果
# QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr recursive

# 预览数据
ipfs cat QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr

# 从 ipfs 下载

ipfs get QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr

# 结果
# Saving file(s) to QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr
#  28.07 MB / 28.07 MB [===========================================================] 100.00% 0s

# 解密

gpg --decrypt QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr > test.pdf

# 检查结果
du -sh *

# 28M	QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr
# 30M	test.pdf
```

打开浏览器，输入 http://localhost:5001/webui 你会看到你存储的文件以及连接到 ipfs 服务器的信息  
从 IPFS 网络查看数据: `https://ipfs.io/ipfs/{hash值}`  

``` bash
wget https://ipfs.io/ipfs/QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr
```

等待一段时间后，你就会收到我的加密后的 pdf～  

在另一台服务器下载后  

``` bash
# 首先要分发私钥，不建议这样做，我只是为了测试

# 导入私钥
gpg --import Juntaran.sec.key

# 解密
gpg QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr > test.pdf

# 检验
md5sum test.pdf
# 57f4e4fd59c28ea46a759e5886ef9df3  test.pdf
# 可以看到和最初的文档一致
```

上传了一个未 GPG 加密的 txt 文档  
可以直接翻墙从 IPFS 访问，无需解密: https://ipfs.io/ipfs/QmSnyy9Z934Rwj11tVgyPiQq5v9TgdxPvzavgEfnQWECtm   

``` bash
wget https://ipfs.io/ipfs/QmSnyy9Z934Rwj11tVgyPiQq5v9TgdxPvzavgEfnQWECtm
cat QmSnyy9Z934Rwj11tVgyPiQq5v9TgdxPvzavgEfnQWECtm

# Hello IPFS from Juntaran
```

## 6 扩展

### 6.1 Filecoin

为什么把 IPFS 放在这里呢，因为这是一个落地的应用，而不是无谓的浪费电力  
有人提出了 `Filecoin` 作为 IPFS 的激励系统，也就是 IPFS 的代币  
Filecoin 也是基于区块链的产物，在 Filecoin 中，矿工不通过大量计算来进行工作证明  
矿工的任务是存储，工作量也就等价于复制量    

### 6.2 对韭当割

迅雷的 `玩客云` 也类似于 IPFS，搞了个 `链克` 作为数字资产  
有一种 Filecoin 和 IPFS 关系的感觉  
但是首先，你要花 500 块钱去京东抢一个 `玩客云` 回来  
点开评论，总是给人一种刷评论的感觉，还有人在评论里 2-3 倍价钱倒卖  
突然有了一种连韭菜苗都要割的感觉  


## 7 总结

IPFS 诞生已经几年了，希望能够借着区块链这波热度起飞～  
成为真正的 `InterPlanetary`  

## 8 附录 

gpg 的简单操作

### 8.1 查看密钥
查看公钥：gpg --list-key  
查看私钥：gpg --list-secret-keys  
 
### 8.2 提取密钥：
提取公钥：gpg -a --export newkey > newkey.asc  
提取私钥：gpg -a --export-secret-keys newkey > newkey_pirv.asc  
 
### 8.3 导入密钥
导入公钥或私钥：gpg --import newkey  
 
### 8.4 使用公钥加密文件：
gpg -ea -r newkey filename  
即会生成 filename.asc 的加密文件  
 
### 8.5 使用私钥解密
gpg -o filename -d filename.asc  
输入私钥密码  
即可把 filename.asc 的加密文件解密成 filename 文件  

### 8.6 删除密钥
删除私钥 
gpg --delete-secret-key newkey  
删除公钥 
gpg --delete-key newkey   

## 9 Reference

- [IPFS White Paper](https://hacpai.com/forward?goto=https%3A%2F%2Fgithub.com%2Fipfs%2Fpapers%2Fraw%2Fmaster%2Fipfs-cap2pfs%2Fipfs-p2p-file-system.pdf)
- [IPFS](https://github.com/ipfs/papers/)
- [IPFS 入门笔记](https://hacpai.com/article/1511015097370)
- [IPFS：替代HTTP的分布式网络协议](http://www.infoq.com/cn/articles/ipfs)
- [How To Use GPG on the Command Line](http://blog.ghostinthemachines.com/2015/03/01/how-to-use-gpg-command-line/)
- [gpg 使用说明](http://blog.csdn.net/cca306/article/details/46501113)
- [Linux下 GPG 的简单使用](http://blog.itpub.net/26355921/viewspace-1248091/)
