# 循序渐进Linux 4：Linux服务器网络配置

*2016.11.9*

## 一、网卡驱动的安装

### 1. 网卡驱动安装的一般思路

 1. 首先从硬件下手，检查网卡本身故障
 2. 检查网卡芯片型号，可以打开机箱查看，也可利用命令查看

        lspci

 3. 查看系统是否包含对应型号网卡驱动

        ll /lib/modules/3.10.0...x86_64/kernel/drivers/net/

4. 查看网卡驱动是否加载
    
        lsmod
> 如果后面是unused，则表示该模块当前没有使用  
> 如果后面是autoclean，则该模块可以使用rmmod -a自动卸载

5. modprobe、insmod/rmmod、depmod
modprobe其实调用了insmod/rmmod与depmod

        modprobe [选项] 模块文件


        
| 选项  | 说明  |
|---|---|
| -r 或 --remove  | 指定模块则卸载该模块，否则自动清除  |
| -l 或 --list  | 显示所有可用模块  |
| -c 或 --show-conf  | 显示所有模块设置信息  |
| -K 或 --autoclean  | 把模块设为自动清除模式  |
| -a 或 -all  | 加载一组匹配的模块  |
| -n 或 --show  | 仅显示要执行的操作  |
| -v 或 --verbose  | 执行时显示详细信息  |
| -q 或 --quiet  | 不显示错误信息  |

如果A模块依赖B模块，modprobe会同时加载A和B，而insmod只会载入指定模块

        insmod [选项] 模块名称或模块文件
        rmmod [选项] 模块名称或模块文件

depmod分析载入模块的相关性

        depmod [选项] 模块名称


### 2. 安装网卡

1. rpm -ivh 网卡.rpm
2. rpm文件默认安装到 `/root/rpmbuild/RPMS`下，把生成的模块文件复制到  `/lib/modules/3.10.0...x86_64/kernel/drivers/net/`
3. 加载驱动

        insmod /lib/modules/3.10.0...x86_64/kernel/drivers/net/bnx2.ko
        或
        modprobe bnx2

4. 查看是否加载

        lsmod | grep bnx2

5. 激活网卡

        ifconfig eth0 up
        ifconfig -a

## 二、 配置Linux网络

### 1. 不同Linux发行版网络配置文件

- RHEL/CentOS:

        /etc/sysconfig/network-scripts/ifcfg-eth0  # 网卡配置文件
        /etc/sysconfig/network-scripts/ifcfg-lo    # 网卡回环地址
        /etc/sysconfig/network                     # 主机名和网关配置文件
        /etc/resolv.conf                           # DNS配置文件
        /etc/hosts                                 # 设置主机和IP绑定信息


- Debian/Ubuntu:

        /etc/network/interfaces                    # 网卡配置文件
        /etc/hostname                              # 主机名和网关配置文件
        /etc/resolv.conf                           # DNS配置文件
        /etc/hosts                                 # 设置主机和IP绑定信息

### 2. 网络配置文件

 - CentOS/RHEL:
修改完网卡配置文件后

        service network restart
        ifconfig eth0 down->up


- Ubuntu/Debian:
修改完网卡配置文件后

        sudo /etc/init.d/networking restart


## 三、Linux网络应用

### 1. Linux下IP别名功能，一块网卡绑定多个IP

- CentOS/RHEL:
在`/etc/sysconfig/network-scripts`目录创建一个`ifcfg-eth0:0`文件并配置相应IP信息即可

        ifconfig [device] [IP] netmask [netmask ip] [up|down]
        ifconfig eth0:1 192.168.66.131 netmask 255.255.255.0 up

- Ubuntu/Debian:
网卡配置信息存放在同一个文件 /etc/network/interfaces


### 2. 开启Linux代理转发功能

- 临时开启，重启失效

        cat /proc/sys/net./ipv4/ip_forward    # 0是禁止转发，1是开启转发
        echo "1" >/proc/sys/net/ipv4/ip_forward

- 永久开启

        sudo vim /etc/sysctl.conf
        net.ipv4.ip_forward = 0    # 改成1
        sudo sysctl -p

### 3. 路由的概念与配置

Linux配置的路由都属于静态路由，即手动输入的方式加入的路由规则  
动态路由无需输入，路由软件自控

    route [-n|-ee]
    route add [-net|-host] [网络或主机] netmask [mask] [gw|dev]
    route del [-net|-host] [网络或主机] netmask [mask] [gw|dev]

| 选项  | 说明  |
|---|---|
| -n  | 不使用通讯协议或主机名，直接使用IP地址  |
| -ee  | 显示更详细的路由信息  |
| add  | 添加路由  |
| del  | 删除路由  |
| -net  | 添加一个网络，后面跟网络号地址  |
| -host  | 后面接的是连接到单独主机路由  |
| netmask  | 后面接子网掩码  |
| gw  | 网关IP  |
| dev  | 指定由哪个网络设备连出去，后面接网络设备名，eth0  |

使用route添加路由的时候，设定的路由必须与自己系统的网络接口或IP可以直接互通





