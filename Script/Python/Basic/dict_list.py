'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/7/25 13:42
'''
# !/usr/bin/env python3
# coding=utf-8

people = {"Alice": {"phone": "2314", "addr": "Foo drive 23"},
          "Beth": {"phone": "1236", "addr": "Bar street 25"},
          "Cecil": {"phone": "8754", "addr": "Bab aser 08"}}
labels = {"phone": "phone number", "addr": "address"}
name = input("name:")
request = input("phone number(p) or address (a)?")
if request == "p": key = "phone"
if request == "a": key = "addr"

if name in people :
    print("%s's %s is %s," % (name,labels[key], people[name][key]))

# 下面用get()提取默认值，get()的好处是get访问一个不存在的键时，不会出现异常错误提示,而是输出NONE或者在get()中给出的值
person = people.get(name, {})  # get(键，{}),建立person映射people字典{name:值}(这种是叫映射对吧--!?)
label = labels.get(key, key)
result = person.get(key, "not available")   # key 不存在时，输出"available"

print("%s's %s is %s" % (name, label, result))