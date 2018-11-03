#!/usr/bin/env python3
#coding:utf-8

import re , datetime , json
import requests

def get_google_head(header_str):
    header_list=header_str.split('\n')
    header_dict=dict()
    for item in header_list:
        b=item.strip(':').split(':',1)
        header_dict[b[0].strip()]=b[1].strip()
    headers={
            'Referer':header_dict.get('referer'),
            'origin':header_dict.get('scheme')+'//'+header_dict.get('authority'),
            'Accept-Encoding':header_dict.get('accept-encoding'),
            'Connection':'keep-alive',
            'Accept':header_dict.get('accept'),
            'User-Agent':header_dict.get('user-agent'),
            'Host':header_dict.get('authority'),
            'Accept-Language':header_dict.get('accept-language'),
            'Cookie':header_dict.get('cookie'),
    }
    token = re.findall('token=(.*?)&', header_dict['path'])[0]
    return token,headers

def get_headers(headers_str):
    headers_list=headers_str.split('\n')
    headers={}
    for item in headers_list[1:]:
        split_list=item.split(':',1)
        headers[split_list[0].strip()]=split_list[1].strip()
    token=re.findall('token=(.*?)&',headers_str)[0]
    return (token,headers)

def get_date(days):
    return (datetime.date.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')

def get_device_name(device):
    device=int(device)
    if device==2:
        device_name='无线'
    elif device==1:
        device_name='PC'
    elif device==0:
        device_name='所有'
    return device_name

def dictPrint(dict_data,width=30):
    for key in dict_data:
        print('{}{}:{}'.format(key,' '*(width-len(key)*2),dict_data[key]))
    print('-'*width*2)


def get_web(url,params=None, headers=None):
    web_data = requests.get(url, headers=headers, params=params)
    return web_data.text

def get_web_to_json(url,params=None, headers=None):
    web_data = requests.get(url, headers=headers, params=params)
    json_data=json.loads(web_data.text)
    return json_data