'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 8:30
'''
# !/usr/bin/env python3
# coding=utf-8

import dns.resolver

domain = input('Please input an domain: ')
NS = dns.resolver.query(domain, 'NS')
for i in NS.response.answer:
    for j in i.items:
        print(j.to_text())

# 只能输入一级域名，比如baidu.com。输入二级或多级域名如www.baidu.com会错误