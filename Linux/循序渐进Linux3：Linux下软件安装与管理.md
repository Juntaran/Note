# 循序渐进Linux 3：Linux下软件安装与管理

*2016.11.8*

## 一、源码安装

    ./configure
    make
    make install


## 二、RPM包
### 1. 安装软件包
    rpm -i [辅助选项] file1.rpm file2.rpm

主选项 -i：　　install，安装  
辅助选项：

| 辅助选项  | 说明  |
|---|---|
| -v  | 显示附加信息  |
| -h  | 安装时输出标记 #  |
| --test  | 测试，不实际安装  |
| --nodeps  | 不检查依赖关系  |
| --force  | 忽略软件包以及软件冲突  |
| --replacepkgs  | 强制重新安装  |
| --prefix  | 把软件包安装到prefix选项指定的路径  |
| --percent	  | 以百分比形式输出安装进度  |
| --excludedocs  | 不安装软件包中说明文件  |
| --includedocs  | 安装软件包包含说明文件  |

### 2. 查询软件包

    rpm -q [辅助选项] package1...packageN

| 辅助选项  | 说明  |
|---|---|
| -f  | 查询操作系统某个文件属于哪个对应的rpm包  |
| -p  | 查询以 .rpm 为后缀的软件包安装后对应的包名称  |
| -l  | 显示软件包中所有文件列表  |
| -i  | 显示软件包概要信息  |
| -g  | 查询系统有哪些软件包属于指定类别  |
| -d  | 显示软件包的说明文件列表  |
| -s  | 在 -l 的基础上显示每个文件的状态  |
| -R 或 --requries  | 显示软件包所需的功能  |
| --provides  | 显示软件包提供的功能  |

### 3. 验证软件包

    rpm -V [辅助选项] package1...packageN

### 4. 更新软件包

    rpm -U [辅助选项] file1.rpm ... fileN.rpm

### 5. 删除软件包

    rpm -e [辅助选项] package1 ... packageN

| 辅助选项  | 说明  |
|---|---|
| --test  | 只执行删除测试  |
| --nodeps  | 不检查依赖性  |


## 三、yum安装方式

    rpm -qa|grep yum    # 检查yum是否安装

    rpm -ivh yum-*.noarch.rpm    # 安装yum

    yum install xxx                               # 安装
    yum remove xxx                             # 删除
    yum check-update                          # 检查更新
    yum update                                    # 更新所有rpm包
    yum update kernel kernel-source  # 更新内核
    yum upgrade                                 # 升级版本
    yum info                                        # 查询RPM包信息

## 四、二进制软件安装

这种格式的软件的安装其实就是解压

    # *.tar.gz格式
    tar -zxvf xxx.tar.gz
    
    # *.bz2格式
    tar -jxvf xxx.tar.bz2


