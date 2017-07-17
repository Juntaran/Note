#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Mon 17 Jul 2017 11:51:50 AM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

# 对 nginx 日志记录的 ip 根据连接次数进行倒序排序

cat /usr/local/nginx/logs/access.log | awk '{print $1}' | sort -n | uniq -c | sort -rn
