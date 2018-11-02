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
import json, re, os

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

def save_image(url, path , name=''):
    extensions = '\.(jpg|gif|jpeg|bmp|png)'
    if not os.path.exists(path):
        os.makedirs(path)
    extension = re.search(extensions, url).group(1)  if re.search(extensions, url) else 'no_ext'
    file_name = os.path.join(path, name + '.' + extension)
    with open(file_name, 'wb') as fs:
        fs.write(requests.get(url, stream=True).content)
        print('{} is download'.format(file_name))

if __name__ == '__main__':
    #num_id = '563155760366'
    #name = 'test'
    num_id = input("请输入商品数字ID:")
    name = input("商品名称设置：")
    input_path = input("商品保存路径，回车默认为程序默认路径")
    path = 'd:\\淘宝抓图\\' + name if not input_path else input_path
    images_url = get_m_dtail_images(num_id)
    image_xuhao = 1
    for image_url in images_url:
        str_xuhao = str(image_xuhao) if image_xuhao>9 else '0'+str(image_xuhao)
        image_name = name + '_' + str_xuhao
        save_image(image_url, path, image_name)
        image_xuhao += 1

