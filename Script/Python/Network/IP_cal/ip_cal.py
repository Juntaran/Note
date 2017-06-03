'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/2 23:23
'''
# !/usr/bin/env python3
# coding=utf-8

from IPy import IP

# 输入IP地址或者网段地址
ip_s = input('Please input an IP or net-range: ')
ips = IP(ip_s)
if len(ips) > 1:    # 为一个网络地址
    print('net: %s' % ips.net())
    print('netmask: %s' % ips.netmask())
    print('broadcast: %s' % ips.broadcast())
    print('reverse address: %s' % ips.reverseNames()[0])
    print('subnet: %s' % len(ips))
else:               # 为一个IP地址
    print('reverse address: %s' % ips.reverseName())

print('hexadecimal: %s' % ips.strHex())     # 十六进制地址
print('binary ip: %s' % ips.strBin())       # 二进制地址
print('iptype: %s' % ips.iptype())          # 地址类型