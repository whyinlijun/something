#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@file: get_sale_detail.py
@time: 2018/4/20 11:09
@desc: 本程序爬取生意参谋单品sku销售数据

商品详情页信息
https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=567069635897&sellerId=99778076&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess

'''

import json,re
import time,datetime
import requests,sqlite3

class Sycm:
    def __init__(self,num_iid,headers_str):
        self.data=[]
        self.num_iid = num_iid
        self.header = {}
        self.token = re.findall('token=(.*?)&', headers_str)[0]
        end_date = datetime.date.today() - datetime.timedelta(2)
        self.payload = {
            '_:': '{:.0f}'.format(time.time() * 1000),
            'itemId': num_iid,
            'device': 2,
            'dateType': 'day',
            'dateRange': '{}|{}'.format(end_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
            'token': self.token,
            'order': 'desc',
            'orderBy': 'skuOrderItemQty',
            'page': 1,
            'pageLimit': 5,
            't': '{:.0f}'.format(time.time() * 1000),
        }
        for item in headers_str.split('\n')[1:]:
            # google浏览器请求头会有以：开始的，如果检测到就去掉
            item = item.strip(':')
            split_list = item.split(':', 1)
            self.header[split_list[0]] = split_list[1].strip()

    def get_sku_prop(self):
        url = 'https://item.taobao.com/item.htm?id={}'.format(self.num_iid)
        t = requests.get(url,headers = self.header)
        rc_skuid = re.compile(r'skuMap\s+:\s*(\{.*\})', re.M)
        rc_skuname = re.compile(r'propertyMemoMap\s*:\s*(\{.*\})', re.M)
        sku_id = re.search(rc_skuid, t.text).group(1)
        sku_name = re.search(rc_skuname, t.text).group(1)
        sku_id = json.loads(sku_id)
        sku_name = json.loads(sku_name)
        self.sku_prop = {}
        for item in sku_id:
            sku = item.split(';')
            self.sku_prop[sku_id[item]['skuId']] = (sku_id[item]['skuId'], sku_name[sku[2]], sku_name[sku[1]])


    def get_data(self,date_str=''):
        url = 'https://sycm.taobao.com/bda/items/itemanaly/sku/getSalesDetails.json'
        if date_str:
            self.payload['dateRange'] = '{}|{}'.format(date_str,date_str)
        while True:
            t = requests.get(url, headers=self.header, params=self.payload)
            content = json.loads(t.text)
            if  'data' in content:
                print("读取第{}页内容中....".format(self.payload['page']))
                self.data.extend(content['data']['data'])
                '''
                for item in content['data']['data']:
                    self.data.append(item)
                '''
                if (content['data']['recordCount']>self.payload['page']*5):
                    self.payload['page'] += 1
                else:
                    break
            else:
                break
            time.sleep(1)

    def save_db(self):
        self.get_sku_prop()
        for item in self.sku_prop:
            print(item)
        b = []
        for item in self.data:
            b.append((
                self.num_iid,
                item['skuId'],
                item['skuName'].split(';')[1],
                self.sku_prop[str(item['skuId'])][1],
                datetime.date.today().strftime("%Y-%m-%d"),
                item['skuNewAddCartItemCnt'],
                item['skuOrderItemQty'],
                item['skuOrderBuyerCnt'],
                item['skuPayItemQty'],
                item['skuPayBuyerCnt']
            ))
        conn = sqlite3.connect('shopdata.db')
        conn.execute("drop table sale_detail")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS sale_detail ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "num_id varchar(20),"
            "sku_id varchar(20),"
            "尺码 varchar(20),"
            "颜色 varchar(20),"
            "日期 datetime,"
            "加购件数 int(8),"
            "下单件数 int(8),"
            "下单人数 int(8),"
            "付款件数 int(8),"
            "付款人数 int(8) "
            ")")
        conn.executemany("INSERT INTO sale_detail(num_id,sku_id,尺码,颜色,日期,加购件数,下单件数,下单人数,付款件数,付款人数) "
                         "VALUES(?,?,?,?,?,?,?,?,?,?)", b)
        conn.commit()
        conn.close()






h =''':authority:sycm.taobao.com
:method:GET
:path:/bda/items/itemanaly/sku/getSalesDetails.json?dateRange=2018-04-19%7C2018-04-19&dateType=recent1&device=2&itemId=567069635897&order=desc&orderBy=skuNewAddCartItemCnt&page=1&pageLimit=5&t=1524240768717&token=d06086b5f&_=1524240768719
:scheme:https
accept:*/*
accept-encoding:gzip, deflate, br
accept-language:zh-CN,zh;q=0.9
cookie:t=3d7703639b8d82d2af085c2896013d93; cookie2=1577a0b595d1474f250b7cfe9734a46e; cna=mclgE1i0QT4CATypk/tPQa+5; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _tb_token_=fe673de041a8b; enc=jGfMe9tdcUkCv0OYQZNEzZpwBz9zBXo%2BUgfAixTNmknxtoNJBZALhGVLqBkqK8qhgntwDkf%2FcLxnn80Q09HcTw%3D%3D; mt=ci%3D-1_1; JSESSIONID=CC0C0F06EE7E8E94F83E5F65DC677369; x=99778076; uc1=cookie14=UoTeOoovJurW0w%3D%3D&lng=zh_CN; uc3=nk2=&id2=&lg2=; tracknick=; sn=liguirong91%3Ack; csg=f1f444c8; unb=2334152358; skt=1750ac61c59ac35a; v=0; _euacm_ac_rs_sid_=35745462; apush30c9ac7d03d7ab7fe36fa8da959ca8fc=%7B%22ts%22%3A1524240768568%2C%22heir%22%3A1524240706164%2C%22parentId%22%3A1524234902855%7D; isg=BEBANjU6DtlnHfLesVvnnwr0EcfSYTtcmJdderrQ_9v3NeRfY92AI6FDSZ31hdxr
referer:https://sycm.taobao.com/bda/items/itemanaly/item_analy.htm?spm=a21ag.7634348.0.0.cf0b7560vycIxD
user-agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'''

c = Sycm(567069635897,h)
c.get_data()
print(len(c.data))
for item in c.data:
    print(item)
c.save_db()
#t = requests.get(url,headers = c.header,params = c.pararms)
#print(t.text)


