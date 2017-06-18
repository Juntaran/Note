#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Sun 18 Jun 2017 09:42:16 AM CST
##########################################

# web服务器防火墙

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

if [[ "$EUID" -ne 0 ]]; then    # check root
    echo 'Root Required' 
    exit 1
fi

# 清空规则
iptables -F
iptables -F -t nat
iptables -X

# 设置默认规则
iptables -P INPUT DROP
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# 加载模块
modprobe iptable_nat
modprobe ip_conntrack_ftp
modprobe ip_nat_ftp

# 每秒钟最多允许100个新连接
iptables -A INPUT -f -m limit --limit 100/sec --limit-burst 100 -j ACCEPT

# 防止Ping-Flood，限制每秒ping包mZ超过10个
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s --limit-burst 10 -j ACCEPT

# 限制SYN等，SYN限制为每秒钟不超过200
iptables -A INPUT -p tcp -m tcp --tcp-flags SYN,RST,ACK SYN -m limit --limit 20/sec --limit-burst 200 -j ACCEPT

# 指定允许连接IP
iptables -A INPUT -s 192.168.1.102 -j ACCEPT

# 打开回环
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT 

# 保存现有连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 开启指定端口
iptables -A INPUT -p tcp -m multiport --dports 80,22 -j ACCEPT 
