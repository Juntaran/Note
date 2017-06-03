'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   17-5-28 下午6:23
'''
# !/usr/bin/env python3
# coding=utf-8

import memcache, random, time, timeit

def compute_square(mc, n):
    value = mc.get('sq:%d' % n)
    if value is None:
        time.sleep(0.001)
        value = n * n
        mc.set('sq:%d' % n, value)
    return value

def main():
    mc = memcache.Client(['127.0.0.1:11211'])
    def make_request():
        compute_square(mc, random.randint(0, 5000))
    print('Ten successive runs:')
    for i in range(1, 11):
        print(' %.2fs' % timeit.timeit(make_request, number=2000), end='')
    print()

if __name__ == '__main__':
    main()
