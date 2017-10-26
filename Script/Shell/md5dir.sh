#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Tue 10 Oct 2017 05:25:25 AM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

# 本脚本放到待计算 md5 值的目录，执行即可
# 最后一行为目录的 md5 值

# 文件较少的时候用这个
# find ./ -type f -print0 | xargs md5sum > md5.temp.txt

# 文件较多的方案
find ./ -type f > document.txt

for d in `cat document.txt`
do
    md5sum $d >> md5.temp.txt
done

cat md5.temp.txt | sort > md5.txt
md5sum md5.txt >> md5.txt
rm -rf md5.temp.txt
rm -rf document.txt
