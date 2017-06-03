'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/3 8:39
'''
# !/usr/bin/env python3
# coding=utf-8

import dns.resolver, httplib2

iplist = []         # 定义域名IP列表变量
appdomain = "www.google.com"     # 定义业务域名

def get_iplist(domain=""):
    try:
        A = dns.resolver.query(domain, 'A')
    except Exception as e:
        print("dns_resolver error:", str(e))
        return False
    for i in A.response.answer:  # 通过response.answer方法获取查询回应信息
        for j in i.items:  # 遍历回应信息
            iplist.append(j.address)
    return True

def check_ip(ip):
    check_url = ip + ":80"
    getcontent = ""
    httplib2.socket.setdefaulttimeout(5)    # 定义http连接超时时间为5s
    conn = httplib2.HTTPConnectionWithTimeout(check_url)    # 创建http连接对象
    try:
        conn.request("GET", "/", headers={"Host": appdomain})   # 发起URL请求，添加host主机头
        r = conn.getresponse()
        getcontent = r.read(15)         # 获取URL页面前15个字符作为可用性校验
    finally:
        if getcontent == "<!doctype html>":     # 监控URL页内容一般为事先定义好的，例如”HTTP200“等
            print(ip, " [OK]")
        else:
            print(ip, " [Error]")       # 可以在这里增加报警程序，比如发送邮件

if __name__ == '__main__':
    if get_iplist(appdomain) and len(iplist) > 0:
        for ip in iplist:
            check_ip(ip)
    else:
        print("dns_resolver error.")