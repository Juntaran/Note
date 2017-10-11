# coding=utf-8

'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/10/11 18:26
'''

# 修改自 https://github.com/yAnXImIN/weiboPicDownloader

import os
import requests
import json

NICKNAMES_FILE = 'weibo_nicknames.txt'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# 读取 nickname
def readNickname():
    # 这里的 nicknames 既可以根据行读，也可以根据空格读
    nicknames = []
    with open(NICKNAMES_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            nicknames.extend(line.split(' '))
    return nicknames

# 把 nickname 转化为 id
def nicknameToContainerid(nickname):
    url = "http://m.weibo.com/n/{}".format(nickname)
    resp = getUrl(url, allow_redirects=False)
    cid = resp.headers['Location'][27:]
    return "107603" + cid

# 根据 url 发起请求
def getUrl(url, stream=False, allow_redirects=True, timeout=10):
    print(url)
    return requests.get(url, headers=HEADERS, allow_redirects=allow_redirects, timeout=timeout)

# 根据 containerid 和 page 把所有图片地址提取出来
def getUrls(containerid, page):
    url = "https://m.weibo.cn/api/container/getIndex?count=25&containerid={}&page={}".format(containerid, page)
    resp_text = getUrl(url=url).text
    json_data = json.loads(resp_text)
    # print(json_data)
    cards = json_data['cards']
    # print(cards)
    photos = []
    if not cards:
        return None
    for card in cards:
        mblog = card.get('mblog')
        if mblog:
            pics = mblog.get('pics')
            if pics:
                for pic in pics:
                    photos.append(pic.get('large').get('url'))
    # print(photos)
    return photos

# 下载图片
def saveImage(nickname, url):
    save_path = os.path.join('WeiboAlbum', nickname)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    image_path = os.path.join(save_path, url.split('/')[-1])
    if os.path.isfile(image_path):
        print("File already exists: " + image_path)
        return

    resp = getUrl(url=url, stream=True)
    image = resp.content
    try:
        with open(image_path, "wb") as image_object:
            image_object.write(image)
            return
    except IOError:
        print("IO Error\n")
        return


# 通过 nickname 开始翻页并保存图片链接
def userRun(nickname):
    cid = nicknameToContainerid(nickname)
    if not cid:
        print("用户名错误")
        return
    all = []
    page = 0
    check = True
    while check:
        page += 1
        urls = getUrls(containerid=cid, page=page)
        check = bool(urls)
        if check:
            print(check)
            all.extend(urls)
    count = len(all)
    index = 0

    for url in all:
        index += 1
        print('{} {}/{}'.format(nickname, index, count))
        # 下载图片
        saveImage(nickname, url)
    pass

if __name__ == '__main__':
    for nickname in readNickname():
        userRun(nickname)