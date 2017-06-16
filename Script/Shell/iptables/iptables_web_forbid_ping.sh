#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 07:16:18 PM CST
##########################################

# 禁止其它机器ping我，我可以ping其它机器
# 开启80 22端口

# 清空规则
iptables -F
iptables -F -t nat
iptables -X

# 加载模块
modprobe ip_tables
modprobe iptable_nat
modprobe ip_nat_ftp
modprobe ip_nat_irc
modprobe ip_conntrack
modprobe ip_conntrack_ftp

# 默认规则处理
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT

# INPUT链处理
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p tcp -m multiport --dports 80,22 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type 0 -j ACCEPT       # icmp-type 0 为响应数据包

# OUTPUT链处理
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -p tcp -m multiport --sport 80,22 -j ACCEPT
iptables -A OUTPUT -p icmp --icmp-type 8 -j ACCEPT      # icmp-type 8 为回显数据包

