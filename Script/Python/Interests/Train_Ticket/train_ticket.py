# coding=utf-8

'''
    Author: Juntaran
    Email:  Jacinthmail@gmail.com
    Date:   2017/8/11 20:45
'''



import argparse
import json
import datetime, time
import prettytable
import requests
from warnings import simplefilter
from requests.packages.urllib3.exceptions import InsecureRequestWarning




'''
车站代号
https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9023

查询余票
https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-08-14&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=HBB&purpose_codes=ADULT
'''


class getStation:
    def __init__(self):
        station_name_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9023'

        try:
            response = requests.get(station_name_url, verify=False)
        except Exception as e:
            print('\033[31mGet Station Error')
            exit()

        ret = response.text.strip()[:-3].split('@')[1:]

        # 创建 {中文:代号} 的字典
        self.stations = {}
        for i in ret:
            item = i.strip().split('|')
            self.stations[item[1]] = item[2]

    def getSymbol(self, name):
        return self.stations[name]

class getTrain:
    def __init__(self, src_station, dst_station, godate):
        self.trains = []
        self.query = {
            'from_station': src_station,
            'to_station': dst_station,
            'train_date': godate
        }
        self.query12306()

    def query12306(self):
        queryUrl = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(godate, src_station, dst_station)

        try:
            ret = requests.get(queryUrl, verify=False)
        except requests.exceptions.Timeout:
            # 超时重连
            time.sleep(3)
            self.query12306()
        else:
            # 如果没有问题，解析返回的 json 数据
            self.parseTrain(ret)

    def parseTrain(self, ret):
        ret = json.loads(ret.text)
        map = ret['data']['map']
        trains = {}
        for i in ret['data']['result']:
            info = i.split('|')
            train_info = {}
            train_info['train_no'] = info[2]
            train_info['train_code'] = info[3]
            train_info['train_start_station'] = info[4]
            train_info['train_end_station'] = info[5]
            train_info['src_station'] = info[6]
            train_info['dst_station'] = info[7]
            train_info['start_time'] = info[8]
            train_info['arrive_time'] = info[9]
            train_info['duration_time'] = info[10]
            train_info['BOOL'] = info[11]
            train_info['train_start_time'] = info[13]
            train_info['train_seat_feature'] = info[14]
            train_info['gjrw'] = info[21] if info[21] else "--"
            train_info['qt'] = info[22] if info[22] else "--"
            train_info['rw'] = info[23] if info[23] else "--"
            train_info['rz'] = info[24] if info[23] else "--"
            train_info['tdz'] = info[25] if info[26] else "--"
            train_info['wz'] = info[26] if info[26] else "--"
            train_info['yw'] = info[28] if info[28] else "--"
            train_info['yz'] = info[29] if info[29] else "--"
            train_info['edz'] = info[30] if info[30] else "--"
            train_info['ydz'] = info[31] if info[31] else "--"
            train_info['swz'] = info[32] if info[32] else "--"

            train_info['src_name'] = map[info[6]]
            train_info['dst_name'] = map[info[7]]
            self.trains.append(train_info)

        table = prettytable.PrettyTable()
        table.field_names = ('车次', '出发车站', '目的车站', '出发时间', '到达时间', '历时', '商务座', '特等座','一等座', '二等座', '高级软卧', '软卧', '硬卧', '软座', '硬座', '无座', '其他')


        for train in self.trains:
            if train['train_start_station'] == self.query['from_station']:
                from_sign = '(始)'
            else:
                from_sign = '(过)'

            if train['train_end_station'] == self.query['to_station']:
                to_sign = '(终)'
            else:
                to_sign = '(过)'

            table.add_row([
                train['train_code'],
                from_sign + train['src_name'],
                to_sign + train['dst_name'],
                train['start_time'],
                train['arrive_time'],
                train['duration_time'],
                train['swz'],
                train['tdz'],
                train['ydz'],
                train['edz'],
                train['gjrw'],
                train['rw'],
                train['yw'],
                train['rz'],
                train['yz'],
                train['wz'],
                train['qt']
            ])
        print(table.get_string())






if __name__ == '__main__':
    simplefilter('ignore', InsecureRequestWarning)
    parse = argparse.ArgumentParser(description='Get Train Tickets')
    parse.add_argument('src', metavar='src', help='Your source station')
    parse.add_argument('dst', metavar='dst', help='Your destination station')
    parse.add_argument('godate', metavar='godate', help='Your departure date')
    args = parse.parse_args()

    # 获取车站代号
    station = getStation()

    # 获取 src 和 dst 的代号
    try:
        src_station = station.getSymbol(args.src)
        dst_station = station.getSymbol(args.dst)
    except KeyError:
        print('\033[31m请输入正确的车站名')
        exit()

    try:
        godate = args.godate
        if datetime.datetime.strptime(godate, '%Y-%m-%d') < datetime.datetime.now():
            raise ValueError
    except:
        print('\033[31m请输入有效日期')
        exit()


    search = getTrain(src_station, dst_station, godate)