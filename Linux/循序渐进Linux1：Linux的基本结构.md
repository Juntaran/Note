# 循序渐进Linux 1：Linux的基本结构

*2016.11.5*

## 一、分区命名：
Linux的硬盘命名方案是基于文件的，一般命名方式如下：

    /dev/hda2
    /dev/sdb3

> /dev：所有设备文件存放目录
> hd与sd：代表分区所在的设备类型。hd代表IDE硬盘，sd代表SCSI硬盘
> a：表示分区在哪个设备上，比如/dev/hda代表第1块IDE硬盘
> 2：代表分区，Linux下前4个分区（主分区或扩展分区）用数字1-4表示，逻辑分区从5开始

 /dev/hda2表示第1块`IDE`硬盘的第2个主分区或扩展分区  
 /dev/sdc6表示第3块`SCSI`硬盘的第2个逻辑分区  
 
 ## 二、Linux控制台
 
 默认Linux下有6个字符控制台，独立作业，互不影响  

Ctrl+Alt+F1~F6切换，Ctrl+Alt+F7从字符界面切换到X-window  

## 三、系统与硬件
### 1. Linux硬件资源管理
#### 1.1 列出所有PCI设备
    lspci
    lspci -v // 更详细

#### 1.2 查看CPU信息
    more /proc/cpuinfo

> processor：   逻辑处理器唯一标识符
> physical id：  每个物理封装的唯一标识符，也就是一个物理CPU
> siblings：　   相同物理封装中的逻辑处理器数量
> core id：　　 每个内核唯一标识符
> cpu cores：　相同物理封装中的内核数量

在`siblings`和`cpu cores`值之间有对应关系，  
如果`siblings`是`cpu cores`的两倍，则说明系统支持超线程，并且已打开  
如果`siblings`与`cpu cores`值相同，则说明系统不支持超线程，或未打开超线程  
查看物理CPU个数、查看每个物理CPU中内核的个数、查看系统所有逻辑CPU的个数（所有物理CPU内核个数+超线程个数）


    // 查看物理CPU个数
    cat /proc/cpuinfo | grep "physical id" | sort | uniq | wc -l

    // 查看每个物理CPU中内核个数
    cat /proc/cpuinfo | grep "cpu cores"

    //查看系统所有逻辑CPU个数
    cat /proc/cpuinfo | grep processor | wc -l



#### 1.3 查看系统内存信息

    more /proc/meminfo

#### 1.4 查看磁盘分区信息

    fdisk -l

### 2. Linux外在设备的使用

设备文件在Linux系统下的/dev下，命名方式是主设备号+次设备号，主设备号说明设备类型，次设备号说明具体指哪个设备

> 软盘：　　/dev/fd(1,2..)
> U盘：　　 /dev/sd(a,b..)(1,2..)　　U盘在Linux下识别为SCSI设备
> 光驱：　　IDE光驱对应/dev/hd(a,b..)，SCSI光驱对应/dev/sr(1,2..)
> 磁带：　　/dev/st(1,2..)

#### 2.1 文件系统类型

|  文件系统格式   |  备注   |
| --- | --- |
|  msdos   |  DOS文件系统类型 |
|  vfat   |  支持长文件名的DOS分区文件系统类型，也可以理解为Windows文件系统类型|
|  iso9660   |  光盘格式文件系统类型 |
|  ext2/ext3/ext4	   |  Linux常见文件系统类型 |
|  xfs   |  Linux下一种高性能日志文件系统，CentOS 7后作为默认文件系统 |

#### 2.2 挂载设备：
    mount -t 文件系统类型 设备名 挂载点

> /mnt:    专门作为临时挂载点目录
> /media: 自动挂载目录

    mount -t msdos /dev/fd0 /mnt/floppu    // 挂载软盘
    mount -t vfat /dev/sda1 /mnt/usb       // 挂载U盘
    mount -t iso9660 /dev/hda /mnt/cdrom   // 挂载光盘
    mount /dev/cdrom /mnt/cdrom            // 挂载光盘
    
    
#### 2.3 卸载设备：
    umount 挂载目录
    umount /mnt/usb            // 卸载U盘
    umount /mnt/cdrom          // 卸载光盘


## 四、文件系统结构

Linux系统以文件的形式全部存放在根目录下，同时分类分层组织成了一个树形目录结构
> **/etc** ：　　存放系统管理相关配置文件以及子目录（重要的有初始化文件/etc/rc 用户信息/etc/passwd 守护进程/etc/crontab DNS配置文件/etc/resolv.conf）  
> **/usr**：　　 主要存放应用程序和文件  
> **/var**：　　 主要存放系统运行与软件运行的日志信息  
> **/dev**：　　主要存放系统设备文件  
> **proc**：　   是一个`虚拟`目录，目录中所有信息都是内存的映射，可以获得进程相关信息并且也可以在系统运行的时候修改内核参数，`/proc目录存在于内存而不是硬盘`  
> **/boot**：　　存放Linux启动文件  
> **/bin与/sbin**：　存放可执行的二进制文件，是binary的缩写。 /bin目录存放的是常用Linux命令，/sbin目录中的s是指超级用户，只有超级用户才能执行这些，常见如磁盘检查修复fcsk，磁盘分区fdisk，创建文件系统mkfs，关机shutdown，初始化系统init  
> **/home**：　 每个用户的工作目录  
> **/lib**：　　   共享程序库与映像文件  
> **/root**：　　 超级用户默认主目录  
> **/run**：　　 外在设备自动挂载点目录，/media与/run基本类似，/mnt是手动挂载点  
> **/lost+found**： 用于保存丢失的文件，比如不恰当关机与磁盘错误导致文件丢失，之后会放在这里，除了/根目录外，每个分区均有这个目录  
> **/tmp**：　　临时文件目录  

## 五、系统服务管理工具systemd

### 1. 启动、停止、重启、重新加载服务

    systemctl start httpd.service            // 启动
    systemctl stop  httpd.service            // 停止
    systemctl restart httpd.service          // 重启（服务没运行则开启）
    systemctl reload httpd.service           // 重新加载配置文件
    
### 2. 查看、禁止、启用服务

这里的启用、禁用服务是指开机启动

    systemctl enable http.service         // 启用服务
    systemctl disable http.service        // 禁止服务





