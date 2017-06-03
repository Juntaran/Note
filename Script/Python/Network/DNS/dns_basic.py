'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-5-28 下午5:49
'''
# !/us=r/bin/env python3
# coding=utf-8

import dns.resolver, argparse

'''
    A:      IPv4
    AAAA:   IPv6
    NS:     名称服务器
    MX:     邮件服务器
    CNAME:  别名
'''

def lookup(name):
    for qtype in 'A', 'AAAA', 'CNAME', 'MX', 'NS':
        answer = dns.resolver.query(name, qtype, raise_on_no_answer=False)
        if answer.rrset is not None:
            print(answer.rrset)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resolve a name using DNS')
    parser.add_argument('name', help='name that you want to look up in DNS')
    lookup(parser.parse_args().name)

# python3 dns_basic.py python.org
# whois python.org