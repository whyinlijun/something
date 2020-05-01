#! /usr/bin/env python3
#coding : utf-8

import requests, re, json
from bs4 import BeautifulSoup

def get_web(url, params):
    with open('cookies.txt') as fs:
        cookies = fs.read().strip()
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
            "referer": 'https://item.taobao.com/item.htm?spm=2013.1.20141001.2.692f4b88ouFoLk&id=592558926894&scm=1007.12144.95220.42296_0_0&pvid=1b2c0fc5-cc7c-4f93-859e-c217d45a7667&utparam=%7B%22x_hestia_source%22%3A%2242296%22%2C%22x_object_type%22%3A%22item%22%2C%22x_mt%22%3A5%2C%22x_src%22%3A%2242296%22%2C%22x_pos%22%3A2%2C%22x_pvid%22%3A%221b2c0fc5-cc7c-4f93-859e-c217d45a7667%22%2C%22x_object_id%22%3A592558926894%7D',
            "cookie": cookies,
        }

        content = requests.get(url, headers=header, params=params)
    return content.text

def get_color(content):
    re1 =re.search('propertyMemoMap\s*:\s*(\{.*?\})',content)
    colors = json.loads(re1.group(1))
    new_sku = {}
    for key in colors :
        if re.search('.*\s.*',colors[key]):
            value1 = colors[key].split()
            new_sku[value1[0]] = [value1[1],key]
        else:
            new_sku[colors[key]] = [colors[key],key]
    return new_sku

def get_size(content):
        soup = BeautifulSoup(content, 'lxml')
        tag = soup.find(attrs={"data-property": "尺码"})
        sizes = tag.find_all('li')
        size = {}
        for item in sizes:
            size[item['data-value']] = item.span.string
        return size

def get_skus(content):
    pass

if __name__ == "__main__":
    num_id = input("请输入商品数字ID: ")
    item_url = 'https://item.taobao.com/item.htm'
    item_params = {
        'id' : '567069635897',
        'spm' : 'a1z10.3-c.w4002-1018448299.41.708d1aeamIGFUp',
    }
    content = get_web(item_url, item_params)
    colors = get_color(content)
    sizes = get_size(content)
    for color in colors:
        print(color,colors[color])
    for key in sizes:
        print(key,sizes[key])
    sku_url = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm'
    sku_params =  {
        'itemId' : num_id,
        'modules' : 'dynStock, soldQuantity',
    }
    sku_content = get_web(sku_url, sku_params)
    print(sku_content)

    '''
    with open('sku.txt', 'w') as f:
        f.write('........' * 10+'\n')
        for item in new_sku:
            print("{}:\t{}".format(item,new_sku[item]))
            f.write("{}:\t{}\n".format(item,new_sku[item][0]))
        f.write('........' * 10+'\n')
    '''



