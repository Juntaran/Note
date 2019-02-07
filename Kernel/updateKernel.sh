#!/bin/bash

# Reference:
# https://blog.csdn.net/zxhio/article/details/80312316
# https://blog.csdn.net/weixin_36796040/article/details/79561836

# 磁盘空间至少 40G

mkdir -p ~/kernel
cd ~/kernel
wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.20.7.tar.xz
tar -xvf linux-4.20.7.tar.xz
cd ~/kernel/linux-4.20.7/
sudo apt-get install bison -y
sudo apt-get install flex -y
sudo apt install make -y
sudo apt install make-guile -y
sudo apt install libncurses-dev -y
sudo apt-get install libssl-dev -y
sudo apt-get install vim

# 默认配置，save 后 exit
make menuconfig

# 分步骤安装
# 4线程编译
#make -j 4 && make modules_install
#
# 安装内核模块
#sudo make modules_install
#
# 安装内核
#sudo make install
#
#sudo apt-get install linux-headers-$(uname -r)

# 合并一步
sudo make bzImage -j 4 && make modules && make modules_install && make install

reboot