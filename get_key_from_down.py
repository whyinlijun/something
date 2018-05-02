#!/usr/bin/env python3
#coding:utf-8

import json
import requests
'''
url='https://suggest.taobao.com/sug?code=utf-8&q=&_ksTS=1490160438326_1388&callback=jsonp1389&k=1&area=c2c&bucketid=2'
https://suggest.taobao.com/sug?code=utf-8&q=k&_ksTS=1490160544459_1402&callback=jsonp1403&k=1&area=c2c&bucketid=2
https://suggest.taobao.com/sug?code=utf-8&q=%E4%B8%AD%E8%80%81%E5%B9%B4%E5%A5%B3%E8%A3%85&_ksTS=1490160752985_2978&callback=jsonp2979&k=1&area=c2c&bucketid=2
https://suggest.taobao.com/sug?code=utf-8&q=中老年女装&_ksTS=1490850894118_10892&callback=jsonp10893&area=b2c&code=utf-8&k=1&bucketid=16&src=tmall_pc

无线1
https://suggest.taobao.com/sug?area=sug_hot&wireless=2&code=utf-8&nick=&sid=null&callback=jsonp2

https://suggest.m.taobao.com/rpc/hot_key.json?nick=&sid=null&callback=jsonp2
https://suggest.m.taobao.com/rpc/history/get.json?nick=&sid=null&callback=jsonp1

https://suggest.taobao.com/sug?q=a&code=utf-8&area=c2c&nick=&sid=null&callback=jsonp3
https://suggest.taobao.com/sug?q=ad&code=utf-8&area=c2c&nick=&sid=null&callback=jsonp4

https://suggest.taobao.com/sug?q=a&code=utf-8&area=c2c&nick=&sid=null&callback=jsonp3
'''
result_data='''{"result":[["妈妈装春装","636521"],["妈妈装外套","849547"],["妈妈装夏装","493654"],["妈妈装连衣裙","586173"],["妈妈装春装外套","210700"],["妈妈装夏装连衣裙","125541"],["妈妈装夏装套装","96702"],["妈妈装春装连衣裙","136010"],["妈妈装外套春秋","251244"],["妈妈装秋装","1090005"]],"magic":[{"index":"1","type":"tag_group","data":[[{"title":"打底衫"},{"title":"针织衫","type":"hot"}],[{"title":"上衣"},{"title":"连衣裙","type":"hot"}],[{"title":"长袖","type":"hot"},{"title":"中长款"},{"title":"中老年"},{"title":"夏季"},{"title":"宽松"},{"title":"外套"}]]},{"index":"2","type":"tag_group","data":[[{"title":"中长款","type":"hot"},{"title":"短款"}],[{"title":"纯色"},{"title":"开衫"},{"title":"两件套"},{"title":"披肩"},{"title":"大码","type":"hot"},{"title":"通勤"},{"title":"宽松"},{"title":"上衣"}]]},{"index":"3","type":"tag_group","data":[[{"title":"衬衫"},{"title":"连衣裙","type":"hot"},{"title":"上衣"}],[{"title":"打底衫"},{"title":"针织衫","type":"hot"}],[{"title":"宽松"},{"title":"中老年"},{"title":"大码"},{"title":"外套"},{"title":"中长款","type":"hot"}]]},{"index":"4","type":"tag_group","data":[[{"title":"短袖"},{"title":"中长款"},{"title":"长袖","type":"hot"}],[{"title":"中老年"},{"title":"a型"},{"title":"上衣"},{"title":"修身"},{"title":"大码","type":"hot"},{"title":"夏季"},{"title":"宽松"}]]},{"index":"5","type":"tag_group","data":[[{"title":"中长款"},{"title":"长袖","type":"hot"}],[{"title":"纯棉","type":"hot"},{"title":"纯色"}],[{"title":"短款"},{"title":"百搭"},{"title":"上衣"},{"title":"开衫"},{"title":"宽松"},{"title":"大码","type":"hot"}]]},{"index":"6","type":"tag_group","data":[[{"title":"中老年"},{"title":"中长款","type":"hot"}],[{"title":"上衣"},{"title":"大码","type":"hot"},{"title":"礼服"},{"title":"显瘦"},{"title":"短袖"},{"title":"修身"},{"title":"宽松"},{"title":"40-49周岁"}]]},{"index":"7","type":"tag_group","data":[[{"title":"长裤","type":"hot"},{"title":"中长款"},{"title":"裤子"}],[{"title":"上衣"},{"title":"连衣裙","type":"hot"}],[{"title":"夏季"},{"title":"纯棉"},{"title":"修身"},{"title":"短袖","type":"hot"},{"title":"宽松"}]]},{"index":"9","type":"tag_group","data":[[{"title":"短款"},{"title":"中长款","type":"hot"}],[{"title":"纯棉"},{"title":"纯色","type":"hot"}],[{"title":"通勤"},{"title":"开衫"},{"title":"两件套"},{"title":"大码","type":"hot"},{"title":"宽松"},{"title":"上衣"}]]},{"index":"10","type":"tag_group","data":[[{"title":"打底衫"},{"title":"衬衫","type":"hot"}],[{"title":"连衣裙","type":"hot"},{"title":"上衣"}],[{"title":"长袖"},{"title":"中老年"},{"title":"适中","type":"hot"},{"title":"中长款"},{"title":"大码"},{"title":"外套"}]]}],"tmall":"妈妈装"}'''

def to_json(data):
    try:
        json_data=json.loads(data)
    except:
        return None
    return json_data



def zhengli(json_data):
    if len(json_data['result'])>0:
        key_list=[{'key':x[0],'count':x[1]} for x in json_data['result']]
    else:
        return []
    if 'magic' in json_data:
        for item in json_data['magic']:
            hot_key = []
            not_hot_key=[]
            xuhao=int(item['index'].strip('index'))-1
            for xiushi_key_list in item['data']:
                for one_key in xiushi_key_list:
                    if 'type' in one_key:
                        hot_key.append(one_key['title'])
                    else:
                        not_hot_key.append(one_key['title'])
            key_list[xuhao]['hot']=hot_key
            key_list[xuhao]['not_hot']=not_hot_key
    return key_list

def get_web_data(key):
    url='https://suggest.taobao.com/sug?code=utf-8&q={}&area=c2c'.format(key)
    return requests.get(url).text

if __name__=='__main__':
    web_text=get_web_data('中老年裤子')
    json_data=to_json(web_text)
    result_data=zhengli(json_data)
    for item in result_data:print(item)