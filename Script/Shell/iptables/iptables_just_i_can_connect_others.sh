#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 06:36:03 PM CST
##########################################

# 只允许我对其它机器发起连接，其它机器不能连接我

# 清空iptables
iptables -F
iptables -F -t nat
iptables -X
iptables -Z

iptables -P INPUT DROP           # 设置默认规则，丢弃所有进入的数据包
iptables -A INPUT -m state --state NEW -j DROP  # 阻止其它机器对我发起连接，我可以对其它机器发起连接
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT # 保留现有连接
