#! /usr/bin/env python3
#coding : utf-8

'''
本程序获取关键词及相关搜索词数据
'''

import time ,requests
import sycm_config
import sycm_getPublic

url = "https://sycm.taobao.com/mq/searchword/relatedWord.json"
keyword = "羽绒背心女"
days = 1

token, headers = sycm_getPublic.get_google_head(sycm_config.headerString)

params = {
        '_:': '{:.0f}'.format(time.time()*1000),
        'token':token,
        'device': '2',
        'dateType': 'day',       #'recent' + str(days),
        'dateRange': '{}|{}'.format(sycm_getPublic.get_date(days), sycm_getPublic.get_date(days)),
        'keyword': keyword
    }

web_get = requests.get(url, params=params, headers=headers).text
print(web_get)
