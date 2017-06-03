'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-5-24 下午5:27
'''
# !/usr/bin/env python3
# coding=utf-8

import socket, random, argparse, sys

MAX_BYTES = 65535

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(message.encode('ascii'), address)

def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))
    # 客户端在connect()之后就不需要使用sendto()和recvfrom()了，而可以用send()和recv()
    # connect()也解决了客户端混杂问题，客户端不会接收到来自其他服务器的数据包
    # connect()连接一个UDP套接字后，可以使用getpeername()方法获得所连接的地址
    print('Client socket name is {}'.format(sock.getsockname()))
    print('Connect with {}'.format(sock.getpeername()))
    # 0.1秒
    delay = 0.1
    text = 'This is another message'
    data = text.encode('ascii')
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            # 第二次等的时间更久一些
            # 指数退避
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc

        else:
            # 结束，跳出循环
            break
    print('THe server says {!r}'.format(data.decode('ascii')))

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,' 
                                                 ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)