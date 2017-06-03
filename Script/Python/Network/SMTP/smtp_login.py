'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-6-1 下午11:11
'''
# !/usr/bin/env python3
# coding=utf-8

import smtplib, sys, socket
from getpass import getpass

message_template = """To: {}
From: {}
Subject: Test Message from smtp_simple.py

Hello,
This is a test message by Python.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("Syntax: {} server fromaddr toaddr [toaddr...]".format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    username = input("Enter username: ")
    password = getpass("Enter password: ")

    try:
        connection = smtplib.SMTP(server)
        try:
            connection.login(username, password)
        except smtplib.SMTPException as e:
            print("Authentication failed:", e)
            sys.exit(1)
        connection.sendmail(fromaddr, toaddrs, message)
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("Your message may not have been sent!")
        print(e)
        sys.exit(1)
    else:
        s = '' if len(toaddrs) == 1 else 's'
        print('Message sent to {} recipient{}'.format(len(toaddrs), s))
        connection.quit()

if __name__ == '__main__':
    main()

# python3 SMTP/smtp_login.py smtp.sina.com jacinthmail@sina.com 1093130996@qq.com