# IPFS

## 简介

IPFS(InterPlanetary File System)，星际文件系统  
名字很好听，是一个`点对点的分布式版本文件系统`，目标是为了补充(取代) HTTP  
把所有具有`相同文件`系统的计算设备连接在一起  
用`基于内容`的地址替代`基于域名`的地址  
这样用户寻找的不是某个`地址`而是存储在某个地方的`内容`  
无需验证发送者的身份，只验证内容的 hash 值  
从而提升网页速度、更快、更安全  

可以把 IPFS 想象成所有文件数据是在同一个 BitTorrent 群并且通过同一个 Git 仓库存取  

## IPFS 原理

参考 http://www.infoq.com/cn/articles/ipfs  

IPFS 从根本上改变了用户搜索的方式，通过IPFS，用户搜索的是内容  
通过 HTTP 浏览器搜索文件的时候，首先找到服务器的位置（IP地址），然后使用路径名称在服务器上查找文件  
按照这个设计，只有文件所有者可以判断这是否是用户要找的文件  
此时，必须保证托管者不会通过移除文件或者关闭服务器而对文件做任何更改  

当文件被添加到 IPFS 节点上，它得到一个新的名字，这个名字实际上是一个加密哈希，它是从文件内容中被计算出来  
通过加密保证该哈希始终只表示该文件的内容。哪怕只在文件中修改一个比特的数据，哈希都会完全不同  

向 IPFS 分布式网络询问哈希的时候，它通过使用一个分布式哈希表  
可以快速（在一个拥有 10,000,000 个节点的网络中只需要 20跳）地找到拥有数据的节点  
从而检索该数据，并使用哈希验证这是否是正确的数据  

IPFS 是通用的，并且存储限制很少。它服务的文件可大可小  
对于一些大的文件，它会自动将其切割为一些小块，使 IPFS 节点不仅仅可以像 HTTP 一样从一台服务器上下载文件，而且可以从数百台服务器上进行同步下载  
IPFS 网络是一个细粒度的、不可靠的、分布式的、易联合的内容分发网络（Content Delivery Network , CDN）  
对于所有数据类型都是很有用的，包括图像、视频流、分布式数据库、操作系统、blockchains 等，而对于 IPFS 来说，最重要的是静态 web 网站  

IPFS 文件也可以是特殊的 IPFS 目录对象，它允许用户使用人类可读的文件名，透明地链接到其他 IPFS 哈希  
用户可以通过默认方式加载目录中的 index.html，这也是标准的 HTTP 服务器采用的方式  
使用目录对象，IPFS可允许用户采用完全相同的方式生成静态网站  
将 web 网站添加到 IPFS 节点中只需要 `ipfs add -r yoursitedirectory`  
在此之后，用户可以从任何 IPFS 节点访问，而不需要链接到 HTML 上的任何哈希  

## 前提

- 自备翻墙 :L  
- Mac | Linux (虽然 Windows 也支持，但是我并不想研究)  
- Go (最好有，如果喜欢源码编译的话)

## 安装 gpg

参考 http://blog.ghostinthemachines.com/2015/03/01/how-to-use-gpg-command-line/ 安装  

``` sh
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

```
gpg --export --armor jacinthmail@gmail.com > mypubkey.asc
```

可以使用以下命令导入你生成的 pubkey:  

```
gpg --import pubkey.asc
```

列出 key:   

```
gpg --list-keys
```

## 安装 IPFS

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

打开浏览器，输入 http://localhost:5001/webui 你会看到你存储的文件以及连接到 ipfs 服务器的信息  
从 IPFS 网络查看数据: https://ipfs.io/ipfs/QmaAHZbevQL9wRUVAWEeUmxkkqftTrffnmRN2GszBVGKVr  

## Reference

- [IPFS White Paper](https://hacpai.com/forward?goto=https%3A%2F%2Fgithub.com%2Fipfs%2Fpapers%2Fraw%2Fmaster%2Fipfs-cap2pfs%2Fipfs-p2p-file-system.pdf)
- [IPFS](https://github.com/ipfs/papers/)
- [IPFS 入门笔记](https://hacpai.com/article/1511015097370)
- [IPFS：替代HTTP的分布式网络协议](http://www.infoq.com/cn/articles/ipfs)