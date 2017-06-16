#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Fri 16 Jun 2017 07:32:26 PM CST
##########################################

# 禁止被ping
iptables -A INPUT -s 0/0 -p icmp --icmp-type 8 -j DROP
