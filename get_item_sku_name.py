#! /usr/bin/env python3
#coding : utf-8

import requests, re, json
from bs4 import BeautifulSoup

def get_web(url):
    return requests.get(url).text

def get_color(content):
    re1 =re.search('propertyMemoMap\s*:\s*(\{.*?\})',content)
    colors = json.loads(re1.group(1))
    new_sku = {}
    for key in colors :
        if re.search('.*\s.*',s[key]):
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


if __name__ == "__main__":
    num_id = input("请输入商品数字ID: ")
    new_sku = get_corlor(num_id)
    with open('sku.txt', 'w') as f:
        f.write('........' * 10+'\n')
        for item in new_sku:
            print("{}:\t{}".format(item,new_sku[item]))
            f.write("{}:\t{}\n".format(item,new_sku[item][0]))
        f.write('........' * 10+'\n')



