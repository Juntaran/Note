'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-5-28 下午4:59
'''
# !/usr/bin/env python3
# coding=utf-8

import socket

print(socket.gethostname())

print(socket.getfqdn())

print(socket.gethostbyname('www.baidu.com'))

print(socket.gethostbyaddr('114.114.114.114'))

print(socket.getprotobyname('UDP'))

print(socket.getservbyname('www'))

print(socket.getservbyport(80))

print(socket.gethostbyname(socket.getfqdn()))