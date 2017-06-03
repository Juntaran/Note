'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 8:33
'''
# !/usr/bin/env python3
# coding=utf-8

import dns.resolver

domain = input('Please input an domain: ')
cname = dns.resolver.query(domain, 'CNAME')
for i in cname.response.answer:     # 结果将回应cname后的目标域名
    for j in i.items:
        print(j.to_text())