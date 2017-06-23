#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Sun 18 Jun 2017 08:35:38 AM CST
##########################################

# 检测局域网存活IP

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

host=$(ifconfig ens33 | grep 'inet ' | sed 's/^.* inet //g' | sed 's/netmask.*$//g' | awk -v FS="." '{$4=null; print $0}' | sed 's/ /./g')

if [ $# -eq 0 ]; then
    temp=$host
else
    temp=$1
fi

for n in {1..254}; do
    hostall=$temp$n
    echo $hostall
    if ping $hostall -c 2 -w 2 >> /dev/null; then
        echo "$hostall is UP"
        echo "$hostall" >> /home/juntaran/workspace/shell/shell/alive.txt
    else
        echo "$hostall is DOWN"
    fi
done
