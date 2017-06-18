#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 07:32:26 PM CST
##########################################

# 禁止被ping

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

if [[ "$EUID" -ne 0 ]]; then    # check root
    echo 'Root Required' 
    exit 1
fi

iptables -A INPUT -s 0/0 -p icmp --icmp-type 8 -j DROP
