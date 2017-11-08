#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Wed 08 Nov 2017 01:44:25 AM EST
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required'
#    exit 1
#fi

# 输出所有指定错误号的日志
cat juntaran.me.log | awk '10==503 {print $0}' > 503.log

# 根据第7列排序去重，输出所有错误接口
cat 503.log| sort -k 7 -u > 503_uniq.log

# 统计最多每秒多少错误
cat 503.log| uniq -c | sort -r | head -n 1

# 清理文件
rm -rf 503* 
