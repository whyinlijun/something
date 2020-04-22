#! /usr/bin/env python3
#coding : utf-8

import requests ,re ,json

def get_sku(num_id):
    url = 'https://item.taobao.com/item.htm?spm=a21ag.7634338.0.0.62cd3dd5J0CGfB&id={}'.format(num_id)

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
    return new_sku

if __name__ == "__main__":
    num_id = input("请输入商品数字ID: ")
    new_sku = get_sku(num_id)
    with open('sku.txt', 'w') as f:
        f.write('........' * 10+'\n')
        for item in new_sku:
            print("{}:\t{}".format(item,new_sku[item]))
            f.write("{}:\t{}\n".format(item,new_sku[item][0]))
        f.write('........' * 10+'\n')



