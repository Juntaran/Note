'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/25 14:24
'''
# !/usr/bin/env python3
# coding=utf-8

# 通过value获取key
def get_keys(data, value):
    return [k for k, v in data.items() if v == value]


# test
# data = {'a': '001', 'b': '002'}
# print(get_keys(data, '001'))