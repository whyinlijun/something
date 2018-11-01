#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@file: save_m_detail_images.py
@time: 2018/10/30 12:11
@desc:

下载保存移动端淘宝商品图片
移动端详情图片获取地址：https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/
参数：
        jsv: 2.4.11
        appKey: 12574478
        t: 1540871646959
        sign: 829fcab0991f6ef02ee09d53914bcab2
        api: mtop.taobao.detail.getdesc
        v: 6.0
        type: jsonp
        dataType: jsonp
        timeout: 20000
        callback: mtopjsonp1
        data: {"id":"563155760366","type":"0","f":"TB1MZOkhH2pK1RjSZFs8quNlXla"}
'''

import requests
import json,re

def get_m_dtail_images(num_id):
    url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/'
    headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "referer": "https: // h5.m.taobao.com / app / detail / desc.html?_isH5Des = true"
    }
    params = {
            #'jsv': '2.4.11',
            #'appKey': '12574478',
           # 't': '1540871646959',
            #'sign': '829fcab0991f6ef02ee09d53914bcab2',
            #'api': 'mtop.taobao.detail.getdesc',
            #'v': '6.0',
            #'type': 'jsonp',
           # 'dataType': 'jsonp',
           # 'timeout': '20000',
            #'callback': 'mtopjsonp1',
            #type 0 为移动版，type 1 为PC版
            'data': '{"id":"'+ num_id  +'","type":"0", "f":"TB1MZOkhH2pK1RjSZFs8quNlXla"}',
    }
    re_compile = re.compile(r'\>(.*)\<')
    web = requests.get(url=url, params=params, headers=headers)
    data = json.loads(web.text)
    images = []
    for image in data['data']['wdescContent']['pages']:
        images.append('https:'+re.search(re_compile, image)[1])
    return images




if __name__ == '__main__':
    num_id = '563155760366'
    a = get_m_dtail_images(num_id)
    print(a)
