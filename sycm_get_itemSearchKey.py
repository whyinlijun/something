#!/usr/bin/env python3
#coding:utf-8

import time
import csv
from getPublic import *
import config

'''
本程序爬取生意参谋的商品关键词分析数据
'''

url='https://sycm.taobao.com/bda/items/itemanaly/itemformto/findItemKeywords.json?'

def get_pararms(token,itemID,page,days=1,web_device='2'):
    '''
    currentPage:2
    dateRange:2017-04-21|2017-04-21
    dateType:recent1
    device:2
    itemId:530945884567
    order:uv
    orderType:desc
    search:
    searchType:taobao
    token:38f507509
    _:1492835423958
    '''
    pararms = {
        '_:': '{:.0f}'.format(time.time()*1000),
        'token':token,
        'device': web_device,
        'dateType': 'day',       #'recent' + str(days),
        'dateRange': '{}|{}'.format(get_date(days), get_date(days)),
        'itemId': itemID,
        'order': 'uv',
        'orderType': 'desc',
        'search': '',
        'searchType':'taobao',
        'currentPage': page,
    }
    return pararms

def data_reduction(datas,key_date,itemid,device):
    re_list=[]
    for item in datas:
        reduction={
            '关键词':item['keyword'],
            '浏览量':item['pv'],
            '访客数':item['uv'],
            '平均流览量':item['avgPv'],
            '跳出率':item['bounceRate']*100,
            '支付买家数':item['payBuyerCnt'],
            '支付件数':item['payItemQty'],
            '支付金额':item['payAmt'],
            '支付转化率':item['payRate']*100,
            '日期':key_date,
            '商品ID':itemid,
            '设备':'无线端' if device=='2' or device==2 else 'PC',
            '搜索排名':item.get('avgSeRank'),
            '曝光量':item.get('expose'),
            '点击量':item.get('clickCnt'),
            '点击率':item.get('clickRate')*100 if 'clickRate' in item else None
        }
        re_list.append(reduction)
        dictPrint(reduction)
    return re_list


def save_csv(filename,dict_datas):
    with open(filename,'w',encoding='utf8') as csvfile:
        fieldname=['日期','设备','商品ID','关键词','搜索排名','曝光量', '点击量','点击率','浏览量','访客数','平均流览量','跳出率','支付买家数','支付件数', '支付金额','支付转化率']
        csv_write=csv.DictWriter(csvfile,fieldnames=fieldname)
        csv_write.writeheader()
        csv_write.writerows(dict_datas)
        #for item in dict_datas:
            #csv_write.writerow(item)

def main(str1,itemid,days,device='2'):
    re_list=[]
    token,header=get_google_head(str1)
    while True:
        print(get_date(days))
        page=1
        while True:
            pararms=get_pararms(token,itemid,page,days,device)
            json_data=get_web_to_json(url,pararms,header)
            if 'data' in json_data:
                if len(json_data['data']['list'])>0:
                    re_list.extend(data_reduction(json_data['data']['list'], get_date(days), itemid, device))
                if json_data['data']['totalPage']>page:
                    page+=1
                    time.sleep(3)
                else:
                    break
            else:
                break
        days-=1
        time.sleep(5)
        if days==0:
            break
    return re_list

if __name__=='__main__':
    itemid='530945884567'
    days=1
    device=2
    filename='/home/yinsir/'+itemid+'.csv'
    datas=main(config.headerString,itemid,days,device)





