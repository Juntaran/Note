#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Thu 28 Sep 2017 11:57:46 PM EDT
##########################################

set -o errexit    # 如果有命令运行失败让脚本退出执行
set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

LOG_DIR_BASE="/home/scribed-store/"

ScribeTemp="/home/scribeTemp/"      # scribe 30天之前日志临时存储文件夹

if [ ! -d "$ScribeTemp" ]; then
    mkdir "$ScribeTemp"
fi

# 建立临时文件夹目录
ls $LOG_DIR_BASE > dir_list.txt
for log_dir in `cat dir_list.txt`
do
    if [ ! -d $ScribeTemp$log_dir ]; then
        mkdir $ScribeTemp$log_dir
    fi
done

for log_dir in `cat dir_list.txt`
do
    find $LOG_DIR_BASE$log_dir -mtime +30  -exec mv {} $ScribeTemp$log_dir \;
done

# scp 限速 50M/s
scp -prl 500000 $ScribeTemp 10.108.24.28:/home/scribeTemp/

rm -rf dir_list.txt
rm -rf $ScribeTemp
