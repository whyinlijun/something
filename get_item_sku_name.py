#! /usr/bin/env python3
#coding : utf-8

import requests ,re ,json

url = 'https://item.taobao.com/item.htm?spm=a21ag.7634338.0.0.62cd3dd5J0CGfB&id=569609605234'

web_text = requests.get(url).text

re1 =re.search('propertyMemoMap\s*:\s*(\{.*?\})',web_text)

s = json.loads(re1.group(1))

new_sku = {}
for key in s :
    if re.search('.*\s.*',s[key]):
        value1 = s[key].split()
        new_sku[value1[0]] = [value1[1],key]
    else:
        new_sku[s[key]] = [s[key],key]

for item in new_sku:
    print("{}:{}".format(item,new_sku[item]))



