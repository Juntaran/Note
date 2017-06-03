'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 8:24
'''
# !/usr/bin/env python3
# coding=utf-8

import dns.resolver

domain = input('Please input an domain: ')
A = dns.resolver.query(domain, 'A')
for i in A.response.answer:     # 通过response.answer方法获取查询回应信息
    for j in i.items:           # 遍历回应信息
        print(j.address)

# www.google.com