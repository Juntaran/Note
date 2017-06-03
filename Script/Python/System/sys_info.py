'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/6/2 22:33
'''
# !/usr/bin/env python3
# coding=utf-8

import psutil, datetime

# User:
print('User info:\n', psutil.users())
print('User count:', len(psutil.users()))

# CPU:
# Windows:
# whole = psutil.cpu_times().user + psutil.cpu_times().system + psutil.cpu_times().idle + psutil.cpu_times().interrupt + psutil.cpu_times().dpc
# Linux:
whole = psutil.cpu_times().user + psutil.cpu_times().system + psutil.cpu_times().idle + psutil.cpu_times().iowait
print('\nCPU info:\n', psutil.cpu_times())
print('CPU count:', psutil.cpu_count(), '  Physical Core:', psutil.cpu_count(logical=False))
print('User Time: {}%\n'.format(round(psutil.cpu_times().user/whole * 100, 2)) , psutil.cpu_times().user)
print('System Time: {}%\n'.format(round(psutil.cpu_times().system/whole * 100, 2)) , psutil.cpu_times().system)
# print('Wait IO: {}%\n'.format(round(psutil.cpu_times().iowait/whole * 100, 2)) , psutil.cpu_times().iowait)
print('Idle Time: {}%\n'.format(round(psutil.cpu_times().idle/whole * 100, 2)) , psutil.cpu_times().idle)

# Memory:
mem = psutil.virtual_memory()
print('\nMemory info:\n', mem)
print('Total Memory:\n{}GB'.format(round(mem.total/pow(1024, 3), 2)))
print('Free Memory:\n{}GB'.format(round(mem.free/pow(1024, 3), 2)))

# Disk:
print('\nDisk info:\n', psutil.disk_partitions())
print('Disk IO:\n', psutil.disk_io_counters())
print('Each Disk IO:\n', psutil.disk_io_counters(perdisk=True))
print('Disk Usage:\n', psutil.disk_usage('/'))

# Net:
print('\nNet info:\n', psutil.net_io_counters())
print('Each Net info:\n', psutil.net_io_counters(pernic=True))
print('TCP connection count:', len(psutil.net_connections('tcp')), '   UDP connection count:', len(psutil.net_connections('udp')))

# Others:
print('\nBoot Time:', datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))