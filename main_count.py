#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

from get_item_sale_count import *
from GoodTables import GoodTables
import time

def get_one(num_id,asia_name):
    c = GoodTables()
    sale_detail = get_data(num_id)
    sql = "SELECT * FROM items_data WHERE id=? AND order_date like ?"
    datas = (num_id,time.strftime("%Y-%m-%d")+'%')
    result = c.select_db(sql, datas)
    if result:
        print("{}距{},已售增加：{}件,今日收藏增加{}，月销量增加：{}，目前月售数量{}".format(
            asia_name+result[0][0],
            result[0][4],
            int(sale_detail['sale_count'])-result[0][2],
            int(sale_detail['favorite_count'])-result[0][3],
            int(sale_detail['month_count'])-result[0][1],
            int(sale_detail['month_count'])
        ))
    else:
        data=(
                str(sale_detail['id']),
                int(sale_detail['month_count']),
                int(sale_detail['sale_count']),
                int(sale_detail['favorite_count']),
                time.strftime("%Y-%m-%d %H:%M:%S")
        )
        zhang_wei_fu = ','.join(['?' for x in range(5)])
        inser_sql = "INSERT INTO items_data VALUES({})".format(zhang_wei_fu)
        c.execute_db(inser_sql, data)

def get_all():
    c = GoodTables()
    sql = "SELECT * FROM items_info"
    result = c.select_db(sql)
    return [(item[0],item[8]) for item in result ]

def save_item_info(num_id, asia_name):
    c = GoodTables()
    sale_detail = get_data(num_id)
    sql = "INSERT OR IGNORE INTO items_info VALUES (?,?,?,?,?,?,?,?,?)"
    datas =(sale_detail['id'],
             sale_detail['title'],
             sale_detail['sell_id'],
             sale_detail['category'],
             sale_detail['url'],
             sale_detail['pic'],
             float(sale_detail['price']),
             float(sale_detail['promotion_price']),
             asia_name
             )
    c.execute_db(sql,datas)

if __name__ == "__main__":
    #for itemId in get_all():
        #get_one(itemId)
    #save_item_info('558470001549', '王震男马甲')
    for item in get_all():
        get_one(item[0],item[1])