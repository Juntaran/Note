#!/bin/bash

##########################################
#   Author: Juntaran
#   Email: Jacinthmail@gmail.com
#   Date: Wed 27 Sep 2017 03:18:37 AM EDT
##########################################

# set -o errexit    # 如果有命令运行失败让脚本退出执行
# set -o nounset    # 若有用未设置的变量即让脚本退出执行

#if [[ "$EUID" -ne 0 ]]; then    # check root
#    echo 'Root Required' 
#    exit 1
#fi

# Scribe 旧日志分储

ScribeTemp="/home/scribe30/"      # scribe 30天之前日志临时存储文件夹

if [ ! -d "$ScribeTemp" ]; then
    mkdir "$ScribeTemp"
fi

# 30天之前的压缩日志移动到临时文件夹
find /home/scribed-store-test/ -mtime +30 -name '*.gz' -exec mv {} $ScribeTemp \;

# 切换到临时文件夹，根据文件名创建相应的文件夹
cd $ScribeTemp
# 因为日志格式是 业务+日期，所以使用 201 作为分割，创建每个业务的文件夹
ls | awk -F "-201" '{print $1}' | sort | uniq | xargs -I {} mkdir {}
ls | awk -F "-201" '{print $1}' | sort | uniq > temp.txt
for names in `cat temp.txt`
do
    echo $names
    mv $names* $names
done

# 删除临时记录
rm -rf temp.txt


# scp 限速 50M/s ，传输到备份服务器
# scp 传输之前，做 源->目的 的免密登录
# 源 /root/.ssh/id_rsa.pub 内容，粘贴到目的机 /root/.ssh/authorized_keys 里
# -p 保存文件创建时间、修改时间  -r 目录递归  -l 限速
scp -prl 500000 $ScribeTemp 192.168.1.1:/home/scribe30/
