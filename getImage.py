#!/usr/bin/env python3
#coding:utf-8


import json
import requests

'''
本程序抓取手机淘宝的商品详情
基本信息抓取url
https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/
返回参数取用的有 item,seller,props,rate
详情页抓取url，主要抓取详情页中的图片
https://acs.m.taobao.com/h5/mtop.wdetail.getitemdescx/4.1/
这个必须要带cookies,要不然抓取不了
'''
#url='https://item.taobao.com/item.htm?spm=a1z10.1-c.w4004-13958609945.2.qTkdOL&id=540684324346'
#url_detail='https://acs.m.taobao.com/h5/mtop.wdetail.getitemdescx/4.1/?appKey=12574478&t=1487601904823&sign=b6429f3fe667cb04765a5894fadc7287&api=mtop.wdetail.getItemDescx&v=4.1&isSec=0&ecode=0&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22item_num_id%22%3A%22540684324346%22%2C%22type%22%3A%220%22%7D'
#url='https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?appKey=12574478&t=1487603581396&sign=db90f9c73cc185945ceed40312b7c749&api=mtop.taobao.detail.getdetail&v=6.0&ttid=2016%40taobao_h5_2.0.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22exParams%22%3A%22%7B%5C%22spm%5C%22%3A%5C%220.0.0.0%5C%22%2C%5C%22id%5C%22%3A%5C%22540684324346%5C%22%7D%22%2C%22itemNumId%22%3A%22540684324346%22%7D'
item_id='540684324346'
def get_good_detail(item_id):
    '''
    response['data‘]:
        vertical:问大家
        skuBase：SKU尺码颜色
        props:商品基本信息
        rate:宝贝评价;totalCount：评价总数,rateList:评价列表
        params：B or C ,品牌ID,类目ID
        apiStack:商品头部价格等，促销价格，促销标题 list
        mockData: suk 价格 数量等 str
        seller:店铺信息，好评率，动态评分，粉丝数，旺旺及店铺ID
        resource:问大家
        item:商品信息

    :param item_id:
    :return:
    '''
    url='https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?'
    headers={
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
    'Referer':'https://h5.m.taobao.com/awp/core/detail.htm?spm=0.0.0.0&id='+item_id,
    'Host':'acs.m.taobao.com',
    }

    cookies={
        #'hw':'cn',
        #'cna':'iO4xES8UnmcCATypkphSToW2',
        #'t':'774698604ea4c4e4b84b114d69ecdd6e',
        #'cookie2':'3c74605a6d236bf4a80f6ac59499da0e',
        #'v':'0',
        '_m_h5_tk':'c95978963c9a09078b258a0a3c82184a_1487605179278',
        '_m_h5_tk_enc':'6178bcdad32424f6ab8e4fa3b4089b37',
        #'linezing_session':'OCBaJpNSYZbSy9ub0CL6C3y4_14876018960368DoG_2',
        #'isg':'Aqys-QKo2NQCCczotlXw7z2MfYMCbgcgn2P-VgbtuNf6EUwbLnUgn6KnQ2NW',
        #'l':'Alpa8j4VIaF8Ms-TDsbudui3Kht8i95l'
    }

    data={
        'appKey':'12574478',
        't':'1487603581396',
        'sign':'db90f9c73cc185945ceed40312b7c749',
        'api': 'mtop.taobao.detail.getdetail',
        'v': '6.0',
        'ttid': '2016@taobao_h5_2.0.0',
        'isSec': '0',
        'ecode': '0',
        'AntiFlood': 'true',
        'AntiCreep': 'true',
        'H5Request:':'true',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'callback': 'mtopjsonp1',
        'data': '{"exParams":"{\"spm\":\"0.0.0.0\",\"id\":\"'+item_id+'\"}","itemNumId":"'+item_id+'"}'
    }
    wb_data=requests.get(url,headers=headers,params=data)
    try:
        json_data = json.loads(wb_data.text[11:-1])
    except:
        return None
    if 'item' in json_data['data']:
        return json_data['data']
    else:
        return None

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
    if data:
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

    else:
        print('数据获取错误，请检查')

if __name__=='__main__':
    item_id = '522041057718'
    item_id='543719444356'
    print_good_info(get_good_detail(item_id))