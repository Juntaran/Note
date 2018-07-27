# coding=utf-8

'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2018/7/23 11:55
'''

from pyecharts import Style
from pyecharts import Geo
import json

#读取城市数据
city = []
with open('target.txt', mode='r', encoding='utf-8') as f:
    rows = f.readlines()
    for row in rows:
        if len(row.split(',')) == 5:
            city.append(row.split(',')[2].replace('\n', ''))

def all_list(arr):
    result = {}
    for i in set(arr):
        result[i] = arr.count(i)
    return result

data = []
for item in all_list(city):
    if (item != ''):
        data.append((item, all_list(city)[item]))
        style = Style(title_color = "#fff", title_pos = "center", width = 1200, height = 600, background_color = "#404a59")

cities = []
with open('city.json', 'r', encoding='utf-8') as f:
    city_data = json.load(f)
    for i in city_data:
        cities.append(i)

ret = []

for i in data:
    if i[0] in cities:
        ret.append(i)

print(ret)

geo = Geo('test', **style.init_style)
attr, value = geo.cast(ret)
geo.add("", attr, value, visual_range=[0, 20], visual_text_color="#fff", symbol_size=20, is_visualmap=True, is_piecewise=True, visual_split_number=4)
geo.render()