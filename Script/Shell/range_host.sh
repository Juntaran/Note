#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Mon 31 Jul 2017 10:09:42 PM EDT
##########################################

# 遍历host列表，远程执行命令

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

host_list=("138.128.206.71" "127.0.0.1")  
user="root"  
port="27226"
  
# 本地通过ssh执行远程服务器的脚本  
for host in ${host_list[*]}  
do
	if [ $host = "138.128.206.71" ]; then  
        port="27226"  
    else  
        port="22"  
    fi  
    ssh -t -p $port $user@$host "mkdir -p /usr/game/zero; seq 300 | xargs -i dd if=/dev/zero of=/usr/game/zero/{}.dat bs=1024000 count=1"
done  
