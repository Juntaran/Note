'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-5-28 下午5:04
'''
# !/usr/bin/env python3
# coding=utf-8

import socket, sys,argparse

def connect_to(hostname_or_ip):
    try:
        infolist = socket.getaddrinfo(
            hostname_or_ip, 'www', 0, socket.SOCK_STREAM, 0,
            socket.AI_ADDRCONFIG | socket.AI_V4MAPPED | socket.AI_CANONNAME,
        )
    except socket.gaierror as e:
        print('Name server failure:', e.args[1])
        sys.exit(1)

    print('infolist:', infolist)
    info = infolist[0]
    socket_args = info[0:3]
    address = info[4]
    s = socket.socket(*socket_args)
    try:
        s.connect(address)
    except socket.error as e:
        print('Network failure:', e.args[1])
    else:
        print('Success: host', info[3], 'is listening on port 80')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Try connecting to port 80')
    parser.add_argument('hostname', help='hostname that you want to contact')
    connect_to(parser.parse_args().hostname)

# python3 ping.py python.org