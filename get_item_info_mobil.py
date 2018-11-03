#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@time: 2018/4/26 9:00
@desc: 手机端获取商品信息

'''

import requests ,re ,json

item_id = '567069635897'
def get_data(item_id):
    url = "http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/"
    headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    payload ={
                #'jsv':'2.4.8',
                #'appKey':12574478,
                #'t':1524702918130,
                #'sign':'35a486bbd39c313cb73b606485de34c9',
                #'api':'mtop.taobao.detail.getdetail',
                #'v':'6.0',
                #'ttid':'2016@taobao_h5_2.0.0',
                #'isSec':0,
                #'ecode':0,
                #'AntiFlood':'true',
                #'AntiCreep':'true',
                #'H5Request':'true',
                #'type':'jsonp',
                #'dataType':'jsonp',
                'callback':'mtopjsonp1',
                #'data':'{"exParams":"{\"spm\":\"a1z10.3-c.w4002-1018448299.28.50831aeaL37PWv\",\"id\":\"567069635897\"}","itemNumId":"567069635897"}',
                'data':'{"itemNumId":"'+str(item_id)+'"}',
    }

    w = requests.get(url,headers = headers , params = payload).text
    w_re = re.search("\((.*)\)",w)
    if w_re:
        data = json.loads(w_re.group(1))['data']
    else:
        data ={}
    return data

def myprint(obj):
    if isinstance(obj,dict):
        for item in obj:
            print(item,':',obj[item])
    elif isinstance(obj,list):
        for item in obj:
            print(item)
    else:
        print(obj)

def print_good_info(data):
    sell=data.get('seller')
    rate=data.get('rate')
    props=data.get('props')
    item=data.get('item')
    print('-----------基本信息-----------')
    myprint(item)
    print('-----------商品参数-----------')
    myprint(props['groupProps'][0]['基本信息'])
    print('-----------商品评价-----------')
    myprint(rate)
    print('-----------卖家信息-----------')
    myprint(sell)

def get_item_other_name(item_id):
    data=get_good_detail(item_id)
    for item in data.get('props')['groupProps'][0]['基本信息']:
        if '货号' in item:
            other_name=item['货号']
            break
    return other_name


if __name__=='__main__':
    item_id = '551679569407'
    #item_id=input('item_id:')
    data = get_data(item_id)
    print_good_info(data)