#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Tue 05 Sep 2017 11:19:15 PM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

for host in `cat hostlist.txt`
do
    dig $host A |  grep IN > dig.txt
done
