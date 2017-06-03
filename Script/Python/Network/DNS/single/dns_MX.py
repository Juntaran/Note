'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 8:27
'''
# !/usr/bin/env python3
# coding=utf-8

import dns.resolver

domain = input('Please input an domain: ')
MX = dns.resolver.query(domain, 'MX')
for i in MX:
    print('MX preference =', i.preference, 'mail exchanger =', i.exchange)

# 163.com