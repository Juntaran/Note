'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/25 13:46
'''
# !/usr/bin/env python3
# coding=utf-8

def list_all_dict(data):
    if isinstance(data, dict):  # 使用isinstance检测数据类型
        for key in data:
            value = data[key]
            print("%s : %s" % (key, value))
            list_all_dict(value)  # 自我调用实现无限遍历

person = {"male":{"name":"Shawn"}, "female":{"name":"Betty","age":23},"children":{"name":{"first_name":"李", "last_name":{"old":"明明","now":"铭"}},"age":4}}

list_all_dict(person)