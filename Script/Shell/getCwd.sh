#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Mon 17 Jul 2017 09:49:57 PM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

# 通过pid查找进程位置

pid=`ps aux | grep $1 | grep -v "grep" | awk '{print $2}'`
for i in ${pid}
do
    cwd_path=`ls -l /proc/${i} | grep "cwd ->" | grep -v "grep" | awk '{print $NF}'`
    exe_path=`ls -l /proc/${i} | grep "exe ->" | grep -v "grep" | awk '{print $NF}'`
    echo ${i}:
    echo "exe_path: "${exe_path}
    echo "cwd_path: "${cwd_path}
    break
done
