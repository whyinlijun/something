#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@file: save_good_table.py
@time: 2018/11/6 16:20
@desc:
'''
import sqlite3, os

class GoodTables():

    def __init__(self, path='goodTables.db'):
        if  path != '':
            self.conn = sqlite3.connect(path)
        else:
            self.conn = sqlite3.connect(':memory:')

    def creat_table(self, sql):
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql)

    def run_once(self):
        items_info = '''CREATE TABLE  IF NOT EXISTS `items_info` (
                `id` varchar(20) PRIMARY KEY,
                `title` varchar(40),
                `sell_id` varchar(20),
                `category` varchar(20),
                `url` varchar(100),
                `pic` varchar(100),
                `price` float,
                `promo_price` float
                )'''
        items_data = ''' CREATE TABLE IF NOT EXISTS `items_data`(
                id,
                month_count,
                sale_count_,
                favorite_count,
                order_date date
                )'''
        self.creat_table(items_info)
        self.creat_table(items_data)

    def insert_many(self, sql, values):
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                c.executemany(sql,values)

    def select_db(self, sql):
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                c.execute(sql)
                return c.fetchall()






if __name__ == "__main__":
    c = GoodTables()
    datas =[('商品ID3','TITLE','SELLID','CATEGORY','URL','PCI','198.0','198.0m'),]
    sql = 'INSERT INTO items_info VALUES (?,?,?,?,?,?,?,?)'
    c.insert_data(sql, datas)
    sql = 'SELECT * FROM items_info'
    for item in c.select_db(sql):
        print(item)
