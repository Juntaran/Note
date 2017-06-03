'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   6/4/17 3:14 AM
'''
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import nmap, sys

scan_row = []
input_data = input('Please input hosts and port: ')
scan_row = input_data.split(" ")
if len(scan_row) != 2:
    print("Input errors, example \"192.168.1.0/24 80,443,22\"")
    sys.exit(0)
hosts = scan_row[0]         # 接收用户输入的主机
port  = scan_row[1]         # 接收用户输入的端口

try:
    nm = nmap.PortScanner() # 创建端口扫描对象
except nmap.PortScannerError:
    print("Nmap not found", sys.exc_info()[0])
    sys.exit(0)
except:
    print("Unexpected error:", sys.exc_info()[0])
    sys.exit(0)

try:
    # 调用扫描方法，参数指定扫描主机hosts, nmap扫描命令行参数arguments
    nm.scan(hosts=hosts, arguments=' -v -sS -p '+port)
except Exception as e:
    print("Scan error:", str(e))

for host in nm.all_hosts():     # 遍历扫描主机
    print('------------------------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))   # 输出主机和主机名
    print('State: %s' % nm[host].state())       # 输出主机状态，如up down

    for proto in nm[host].all_protocols():      # 遍历扫描协议，如tcp udp
        print('-------')
        print('Protocol: %s' % proto)           # 输出协议名
        lport = nm[host][proto].keys()          # 获取协议的所有扫描端口
        # lport.sort()                            # 端口列表排序
        for port in lport:                      # 遍历端口并输出端口与状态
            print('port: %s\tstate: %s' % (port, nm[host][proto][port]['state']))

# sudo python3 nmaptest.py
# 192.168.1.0/24 80,443,22