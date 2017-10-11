#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Wed 11 Oct 2017 11:29:33 AM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

# 删除30天之前的文件

find /home/logs -mtime +30 -type f -exec rm -rf {} \;
