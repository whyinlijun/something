#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@file: get_sale_detail.py
@time: 2018/4/25 21:00
@desc: 发现好货,从电脑端猜你喜欢进入的,本程序抓取发现好货页面商品销售数据

各页面的数据逻辑:
        生意参谋数据前一日为没有减掉退款的件数数据
        淘宝搜索页面    付款人数为 前一日结束付款人数之和,已减掉退款人数
        店铺销量排序页面 销售件数, 前一日结束销售件数之和,已减掉退款件数

商品详情页信息
https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=567069635897&sellerId=99778076&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,upp,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess

'''

import requests, re, json, time
import sqlite_console as sql_c

IS_PRINT = False

def get_data(itemID):
    url = "https://tui.taobao.com/recommend"
    headers = {
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    payload = {
                'type': 2,
                'count': 25,
                'itemId': itemID,
                #'scm': '1007.10008.56612.103200300000000',
                'appid': 1502,
                #'_ksTS': '1524663427460_44',
                'callback': 'jsonp45',
    }
    while True:
        w = requests.get(url , params = payload , headers = headers)
        re_c = re.compile("\((.*)\)")
        re_d = re.search(re_c, w.text).group(1)
        re_dict = json.loads(re_d)
        if "orderCost" in re_dict['detail']:
            break
        time.sleep(2)

    if IS_PRINT:
        for item in re_dict['detail']:
            print('{}:{}'.format(item,re_dict['detail'][item]))

    sale_detail = {
        'id': re_dict['detail']['itemId'],
        'title': re_dict['detail']['itemName'],
        'sell_id': re_dict['detail']['sellerId'],
        'category': re_dict['detail']['categoryId'],
        'url': re_dict['detail']['url'],
        'pic': re_dict['detail']['pic'],
        'price': re_dict['detail']['price'],
        'promotion_price': re_dict['detail']['promotionPrice'],
        'sale_count': re_dict['detail']['sellCount'],
        'month_count': re_dict['detail']['monthSellCount'],
        'favorite_count': re_dict['detail']['orderCost'],
    }
    return sale_detail

def main(num_id):
    conn = sql_c.get_conn(sql_c.DB_FILE_PATH)
    #sql_c.init(conn)
    sql = "SELECT * FROM count_items WHERE id = {} AND order_date = '{}'".format(num_id, time.strftime("%Y-%m-%d"))
    result = sql_c.select_sql(conn, sql)
    sale_detail = get_data(num_id)
    if result:
        print("距{},已售增加：{}件,今日收藏增加{}，月销量增加：{}，目前月售数量{}".format(
            result[4],
            int(sale_detail['sale_count'])-result[2],
            int(sale_detail['favorite_count'])-result[3],
            int(sale_detail['month_count'])-result[1],
            int(sale_detail['month_count']
        ))
    else:
        data=[]
        data.append((str(sale_detail['id']),
              int(sale_detail['month_count']),
              int(sale_detail['sale_count']),
              int(sale_detail['favorite_count']),
              time.strftime("%Y-%m-%d")
              ))
        zhang_wei_fu = ','.join(['?' for x in range(5)])
        sql = "INSERT INTO count_items VALUES({})".format(zhang_wei_fu)
        sql_c.insert_order(conn, sql, data)

if __name__ == "__main__":
    while True:
        main('558470001549')
        time.sleep(60*10)
