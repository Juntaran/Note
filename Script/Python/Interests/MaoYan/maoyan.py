# coding=utf-8

'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2018/7/23 11:48
'''

import requests
import json
import time
import random

#下载第一页数据
def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

#解析第一页数据
def parse_one_page(html):
    data = json.loads(html)['cmts']
    for item in data:
        yield{
        'comment':item['content'],
        'date':item['time'].split(' ')[0],
        'rate':item['score'],
        'city':item['cityName'],
        'nickname':item['nickName']
        }

#保存数据到文本文档
def save_to_txt():
    for i in range(1, 1001):
        url = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)
        print('正在保存第%d页。'% i)
        for item in parse_one_page(html):
            with open('source.txt', 'a', encoding='utf-8') as f:
                f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')
        time.sleep(5 + float(random.randint(1, 100)) / 20)

def uniq(infile,outfile):
    infopen = open(infile,'r',encoding='utf-8')
    outopen = open(outfile,'w',encoding='utf-8')
    lines = infopen.readlines()
    list_l = []
    for line in lines:
        if line not in list_l:
            list_l.append(line)
            outopen.write(line)
    infopen.close()
    outopen.close()


if __name__ == '__main__':
    save_to_txt()
    uniq("source.txt", "target.txt")