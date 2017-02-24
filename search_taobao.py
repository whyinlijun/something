#!/usr/bin/env python3
#coding:utf-8

import requests,json

url='https://s.m.taobao.com/search'

data={
    'q':'中老年女裤',
    'search':'提交',
    'tab':'all',
    'sst':'1',
    'n':'20',   #每页数量，默认是20,可以改
    'buying':'buyitnow',
    'm':'api4h5',
    'abtest':'19',
    'wlsort':'19',
    'style':'list',
    'closeModues':'nav,selecthot,onesearch',
    #'sort':'_sale',
    'page':'100',#最大单位是100页
}

wb_data=requests.get(url,params=data)
result=json.loads(wb_data.text)
listitem=result.get('listItem')
if listitem:
    for item in listitem:
        if item['img2'] in item['pic_path']:
            print('yiyangde')
        else:
            print(item['img2'],'----',item['pic_path'])
