---
title: Docker
tags: Docker,容器
grammar_cjkRuby: true
---

*2016.11.22*


# Docker特点
特性：

 1. 资源独立，隔离
 

> 与宿主机其他应用互不影响

 2. 环境一致性
> 无论build的Docker image创建的container在哪里都能够保证环境变量、运行环境相同
 3. 轻量化
> 与虚拟化相比快速开/关机
> CPU/内存的低消耗
> 速度快
 4. Build Once,Run Everywhere
> 只需要迁移符合标准规范

总结就是容器技术的`高生产力`符合当前高产能的需求


----------


## Docker是什么

Docker是一种`容器`技术，把应用和环境打包，形成一个独立的，类似与APP形式的应用。与虚拟化技术类似，极大的方便了应用服务的部署，却又与虚拟化技术不同，它以一种更`轻量`的方式实现了应用服务的打包。使用Docker可以让每个应用彼此相互隔离，在同一台机器上同时运行多个应用。可以在更细的粒度上进行资源的管理，比虚拟化技术更节约资源。

![](https://raw.githubusercontent.com/Juntaran/Note/master/pictures/VMvsDocker.jpg)


   上图是Docker与虚拟机的实现框架，可以很明显看出虚拟机的Guset OS层（虚拟机安装的操作系统）和Hypervisor层（硬件虚拟化平台，比如KVM）在Docker中被Docker Engine所替代。
虚拟机实现资源隔离的方法是独立OS+虚拟化CPU、内存、IO设备。
Docker实现资源隔离的方法是利用`Linux内核本身支持的容器方式实现资源和环境隔离`。
Docker有着更少的抽象层，不需要Hypervisor实现硬件虚拟化，运行在Docker容器上的程序直接使用的都是世纪物理机的硬件资源。因此在CPU、内存利用率上Docker效率更高。
此外，Docker利用宿主机内核`无需Guest OS`，当新建一个容器时无需加载操作系统内核，资源开销相比虚拟机极小，启动/关闭时间也远高于虚拟机。
--------
## Docker的基本概念

 - 镜像——Image
 - 容器——Container
 - 仓库——Repository

**镜像：**
	镜像是一个只读的模版，一个镜像可以包含一个完整的Ubuntu操作系统环境，里面仅安装了Apache或用户需要的其它应用程序，镜像可以用来创建Docker容器
**容器：**
	Docker利用容器来运行应用。
    容器是从镜像创建的运行实例，可以被启动、开始、停止、删除，每个容器都是相互隔离的，可以把容器看作一个简易版的Linux环境
>  镜像是只读的，容器在启动的时候创建一层可写层作为最上层

**仓库：**
	仓库是集中存放镜像文件的场所，仓库注册服务器（Registry）中往往存放多个仓库，每个仓库又包含了多个镜像，每个镜像有不同的标签（tag）
    仓库分为公开库与私有库。
    最大的公开仓库是Docker Hub，国内有Docker Pool等。
    用户也可以在本地网络创建一个私有仓库。
    用户创建了自己的镜像后可以使用`push`上传到仓库，在使用另外一台机器的时候可以从仓库`pull`下来。
    
    

---------
## Docker的使用

> Ubuntu使用提示：
> 一定要用`sudo`

安装Docker

    yum install docker

启动守护进程

    service docker start

在系统启动时运行

    chkconfig docker on
  
获取远程镜像

    docker pull ubuntu

创建一个容器

    docker create
    
运行一个新容器

    docker run

启动一个新容器，并把Ubuntu的shell作为入口

    docker run -it ubuntu:latest sh -c '/bin/bash'
`-i`代表这是一个交互容器，把当前标准输入重定向到容器的标准输入，而不是终止程序运行
`-t`代表为这个容器分配一个中断
`Ctrl+D`可以退出这个容器

    docker ps -a
`docker ps`命令可以看到当前正在运行的容器
`-a`参数可以看到所有创建的容器

退出容器后要重新启动这个容器

    docker start

**注意：
每次执行`docker run`命令都会创建新的容器，最好一次创建后使用`docker start/stop`来启动/停用容器**









----------
**参考/引用来源：**
[DaoCloud][1]
[cbl709][2]
[极客学院][3]


  [1]: http://docs.daocloud.io/
  [2]: http://blog.csdn.net/cbl709/article/details/43955687
  [3]: http://wiki.jikexueyuan.com/project/docker-technology-and-combat/
