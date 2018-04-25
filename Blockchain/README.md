# 从零认识区块链

## 前言

首先，注意本文的标题是《从零认识区块链》，而不是《从零认识虚拟货币》  
对于虚拟货币，我是比较排斥的，尤其是以比特币为代表，基于 POW(proof of work) 的虚拟货币  
浪费硬件资源和电能，做无用的计算，从发白皮书到割韭菜  

那么区块链和虚拟货币的区别在哪里？  
比特币作为区块链的第一个应用，我们可以说比特币是区块链，但是区块链并不是比特币  
本文忽略了`交易`的实现以及算法，重点在于阐释区块链的构造，以及一个应用价值较高的非数字货币的项目  

本文在 NIST(National Institute of Standards and Technology) 于2018年1月的区块链技术综述上，结合作者之前了解的相关理论，以分析区块链的构造为宗旨、以作者的喜好为转移，实现了一个简易版本的区块链并在最后介绍了一个具有 `实际价值` 的落地项目  

## 1 区块链历史

2008年中本聪发表了论文《Bitcoin: A Peer-to-Peero Electronic Cash System》。在该文认为在交易的过程中，两者之间缺乏信任需要引入第三方中介，这样会增加交易成本还会泄露给信息给第三方。于是他提出了比特币挖矿和交易方案  

2009年1月3日，中本聪创世块诞生，留下了当时泰晤士报头版标题 “The Times 03/Jan/2009 Chancellor on brink of second bailout for banks”   

## 2 区块链结构

### 2.1 地址

每个用户都有一个自己的 Address，一个用户的 `address` 是一个简短的、字母+数字形式的字符串，由用户的公钥以及一些其他的数据(用于校验错误)，使用 hash 推导而来，address 用来发送接收数字资产

大多数的区块链系统利用 `to` 和 `from` 作为交易的两端，地址是由公钥经过 hash 后生成的  

用户可以生成许多对 private/public key 用来生成地址，允许不同程度的伪匿名  
在一个区块链中，对于用户来说，地址就是他的 `身份` ，有时候 address 会被转化成二维码从而更方便的使用  

当一个区块链分配数字资产的时候，它通过把资产分配到地址来实现  
为了花费数字资产，一个用户必须证明该 `address` 对应的 `私钥` 的所有权  
通过使用私钥来对一个 `transaction` 进行数字签名，该 transaction 可以通过公钥来验证   

### 2.2 账本

区块链在虚拟货币方向的应用主要是分布式记账，在传统的数据库中，通常由集中“可信”的第三方进行操作，换句话说，这个“第三方”就是账本的拥有者。  

传统记账的缺点:  
- 账本可能丢失或损坏，用户必须相信第三方备份系统的可靠性    
- 交易可能不合法，用户必须相信第三方会合法的处理交易  
- 交易列表可能不完整，用户必须相信第三方记录了完整的交易信息  
- 交易内容可能被改变，用户必须相信第三方不会篡改历史记录  

区块链的改进:  

- 区块链为了解决这些问题，采用了分布式共识机制(distributed consensus mechanism)  
- 区块链账本会被复制到系统中的每个节点  
- 如果有一个新的交易请求提交到某个节点，会通知区块链系统中剩余的节点有一个交易的到达  
- 当系统中有新的用户加入，他会收到一份完整的区块链账本复制  

因此区块链系统丢失或者篡改账本与传统集中第三方处理相比，安全可靠的多  

## 3 Blockchain

一个区块链系统为了创造一个新的 block，会采用一些策略  
比如谁先算出 puzzle 的节点就获得生成下一个 block 的权利  
一旦 puzzle 被解决，该节点会创造 block 的数据并存储同步  

![blockchain](https://raw.githubusercontent.com/Juntaran/Note/master/pictures/blockchain.png)

### 3.1 block

从图中可以看到，一个 block 是由以下组成的:  

区块头:  

- prevHash: 上一个区块 hash  
- Merkle Tree Root Hash  
- timestamp: 时间戳  
- Nonce: 解决 puzzle 的随机数  

区块体:  

- Hash: 对当前区块头的哈希值  
- Transaction List: 交易集合

### 3.2 Merkle Tree

从图中可以看到有一个 Merkle Tree，是一种哈希二叉树  
常见的 Merkle Tree 应用方法是令每一个叶子节点都是 hash 值  
两个叶子节点的父节点是他们求和再次哈希  
Merkle Tree 用于记录一个区块中所有的交易信息  
以比特币为例，每10分钟生成一个区块，在这十分钟内所有的比特币交易会写入 `transaction list`  
区块中任何一笔交易的改变都会修改整个 Merkle Tree  

### 3.3 Nonce

Nonce 是一个随机数，创建一个 block 的时候会对区块头和 nonce 进行哈希计算  
如果验证通过则挖矿成功  
而为了验证通过，只能不断尝试各种随机数，比如难度设置为5，即 `想要哈希值前缀为 00000`，会不断利用新的随机数进行尝试  
因为区块头包含 timestamp，所以不会出现一劳永逸的答案  


## 4 共识算法

1. Pow(proof of work) 工作量证明，浪费算力挖矿  
2. Pos(proof of stake) 权益证明，每个节点所占代币的比例越多，难度越低  
3. R-R(Round Robin) 轮询算法

Pow 与 Pos 都是一种随机选择下一个 block 上传者的方式  
不同的是，Pow 根据计算能力随机 （如果攻击者伪造，需要 51% 的算力）  
Pos 根据拥有财产随机 （如果攻击者伪造，需要拥有 51% 的货币）  

### 4.1 Pow 工作量证明

比特币每2周调整一次 puzzle 难度，每十分钟生成一个新的 block，使用 SHA-256 算法，经测试，难度为 `00000` 时，需要计算 10,730,896 次，用时 54 秒；难度为 `000000` 时，计算了 934,224,175 次，用时 1h18min12s  
根据不同的难度求解很难，但是验证很方便，只需要进行一次 hash ，查一下 hash 结果前缀0的个数就可以判断了  
Pow 的缺点在于浪费了大量的算力、前后期贫富差异过大、浪费电力；优点在于可靠性  

### 4.2 Pos 权益证明

Pos 选择生成 block 节点的方案很有趣，他有一个多轮投票机制，系统会选择几个“股权”用户，然后让所有“股权”用户投票  
Pos 的缺点在于“富人”可以更加容易地获取数字资产，但是在一个系统中获得 >50% 的资产成本极高  

### 4.3 R-R 轮询算法

系统轮询，每个节点都有机会创造新的 block ，当被轮询的节点不可用时，系统会进行随机选择  
轮询的优点在于无需确定一个复杂的共识机制来决定谁产出新 block、保证不会出现某一个节点成为“大多数”、不浪费资源；缺点在于系统中的节点处于某种程度上的互信，在开放式网络中的表现不好，因为恶意节点会持续增加  

### 4.4 冲突解决

多数区块链系统采用 “长者优先” 原则  
冲突一旦发生会很快解决，根据 “长者优先” 的策略确定一个 `offical` 链，再由他增加下一个合法的 block，非该链发生的交易会被添加进来  

### 4.5 写入信息

`Transcation` 就会被当作 `Info` 写入到区块链，例如 https://etherscan.io/tx/0x2d6a7b0f6adeff38423d4c62cd8b6ccb708ddad85da5d3d06756ad4d8a04a6a2

[比特币的第一笔交易](https://btc.com/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f?page=1&asc=1&order_by=outputs_count)

## 5 一个可用的落地项目: IPFS

### 5.1 简介

IPFS(InterPlanetary File System)，星际文件系统  
名字很好听，是一个 `点对点的分布式版本文件系统` ，目标是为了补充(取代) HTTP  
把所有具有 `相同文件` 系统的计算设备连接在一起  
用 `基于内容` 的地址替代`基于域名`的地址  
这样用户寻找的不是某个 `地址` 而是存储在某个地方的 `内容`   
无需验证发送者的身份，只验证内容的 hash 值  
从而提升网页速度、更快、更安全  

可以把 IPFS 想象成所有文件数据是在同一个 BitTorrent 群并且通过同一个 Git 仓库存取  

### 5.2 IPFS 原理

HTTP 可以视为一种集中化的协议，有以下几个缺点:  

1. 容易遭受 DDoS 攻击  
2. 过度依赖于骨干网  
3. 容易被监视审查控制  

HTTP 首先 `基于域名` 寻找服务器 IP 地址，之后根据路径访问资源  
IPFS 则是根据内容哈希，通过底层的 DHT(分布式哈希表) 来快速找到拥有数据的节点  
可以把 IPFS 简单视作为 CDN  

以下摘自 http://www.infoq.com/cn/articles/ipfs  
前人写的已经够好了，无需我再废话  

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

### 5.3 使用前提

- 自备翻墙 :L  
- Mac | Linux (虽然 Windows 也支持，但是我并不想研究)  
- Go Env (最好有，如果喜欢源码编译的话)

### 5.4 安装 GPG

- GPG 的作用在于加密文件，如果不想对共享文件进行加密可以略过  

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

### 5.5 安装 IPFS

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

# 从 ipfs 下载（从当前节点下载，并非从 ipfs 网络下载）

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
# 正常流程应该是用A的公钥由B加密上传，A从 ipfs 网络下载后直接使用A的私钥解密

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

### 5.6 扩展

#### 5.6.1 Filecoin

为什么把 IPFS 放在这里呢，因为这是一个落地的应用，而不是无谓的浪费电力  
有人提出了 `Filecoin` 作为 IPFS 的激励系统，也就是 IPFS 的代币  
Filecoin 也是基于区块链的产物，在 Filecoin 中，矿工不通过大量计算来进行工作证明  
矿工的任务是存储，工作量也就等价于复制量    

#### 5.6.2 对韭当割

迅雷的 `玩客云` 也类似于 IPFS，搞了个 `链克` 作为数字资产  
有一种 Filecoin 和 IPFS 关系的感觉  
但是首先，你要花 500 块钱去京东抢一个 `玩客云` 回来  
点开评论，总是给人一种刷评论的感觉，还有人在评论里 2-3 倍价钱倒卖  
突然有了一种连韭菜苗都要割的感觉  


### 5.7 总结

IPFS 诞生已经几年了，希望能够借着区块链这波热度起飞～  
成为真正的 `InterPlanetary`  

### 5.8 附录 

gpg 的简单操作

#### 5.8.1 查看密钥
查看公钥：gpg --list-key  
查看私钥：gpg --list-secret-keys  
 
#### 5.8.2 提取密钥：
提取公钥：gpg -a --export newkey > newkey.asc  
提取私钥：gpg -a --export-secret-keys newkey > newkey_pirv.asc  
 
#### 5.8.3 导入密钥
导入公钥或私钥：gpg --import newkey  
 
#### 5.8.4 使用公钥加密文件：
gpg -ea -r newkey filename  
即会生成 filename.asc 的加密文件  
 
#### 5.8.5 使用私钥解密
gpg -o filename -d filename.asc  
输入私钥密码  
即可把 filename.asc 的加密文件解密成 filename 文件  

#### 5.8.6 删除密钥
删除私钥 
gpg --delete-secret-key newkey  
删除公钥 
gpg --delete-key newkey   

## 6 总结

如果能看到最后说明你已经浪费了大约 1h 的时间在这里  
本文介绍了区块链的构成以及一些主要的组成部件，在最后宣传了一下 IPFS  
  
一个简易的区块链实现可以参考 https://github.com/Juntaran/EZChain  
闲余时间参考了几个 gayhub 的源码写的 Demo，还未完全实现  

___
## Reference

- [NIST Blockchain Technology Overview](https://csrc.nist.gov/publications/detail/nistir/8202/draft)
- [IPFS White Paper](https://github.com/ipfs/papers/raw/master/ipfs-cap2pfs/ipfs-p2p-file-system.pdf)
- [IPFS](https://github.com/ipfs/papers/)
- [IPFS 入门笔记](https://hacpai.com/article/1511015097370)
- [IPFS：替代HTTP的分布式网络协议](http://www.infoq.com/cn/articles/ipfs)
- [How To Use GPG on the Command Line](http://blog.ghostinthemachines.com/2015/03/01/how-to-use-gpg-command-line/)
- [gpg 使用说明](http://blog.csdn.net/cca306/article/details/46501113)
- [Linux下 GPG 的简单使用](http://blog.itpub.net/26355921/viewspace-1248091/)
