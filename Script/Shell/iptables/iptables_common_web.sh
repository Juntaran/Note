#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 06:57:00 PM CST
##########################################

# 只开放22 80端口

# 清空规则
iptables -F
iptables -X
iptables -Z

# 加载模块
modprobe ip_tables
modprobe iptable_nat
modprobe ip_nat_ftp
modprobe ip_conntrack

# 许出不许进
iptables -P INPUT DROP
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# 打开回环
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# 开放端口
iptables -A INPUT -p tcp -m multiport --dports 22,80 -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
