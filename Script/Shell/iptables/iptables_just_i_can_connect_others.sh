#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 06:36:03 PM CST
##########################################

# 只允许我对其它机器发起连接，其它机器不能连接我

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

if [[ "$EUID" -ne 0 ]]; then    # check root
    echo 'Root Required' 
    exit 1
fi

# 清空iptables
iptables -F
iptables -F -t nat
iptables -X
iptables -Z

iptables -P INPUT DROP           # 设置默认规则，丢弃所有进入的数据包
iptables -A INPUT -m state --state NEW -j DROP  # 阻止其它机器对我发起连接，我可以对其它机器发起连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT # 保留现有连接
