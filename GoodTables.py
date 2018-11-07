#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@time: 2018/11/6 16:20
@desc:
'''
import sqlite3, time

class GoodTables():
    '''
    sqlite3数据增删改查类
    初始化传空字符为表建在内存中
    '''

    def __init__(self, path='goodTables.db'):
        if  path != '':
            self.conn = sqlite3.connect(path)
        else:
            self.conn = sqlite3.connect(':memory:')


    def run_once(self):
        '''执行建表操作'''
        items_info = '''CREATE TABLE  IF NOT EXISTS `items_info` (
                `id` varchar(20) PRIMARY KEY,
                `title` varchar(40),
                `sell_id` varchar(20),
                `category` varchar(20),
                `url` varchar(100),
                `pic` varchar(100),
                `price` float,
                `promo_price` float,
                `asia_name` varchar(40)
                )'''
        items_data = ''' CREATE TABLE IF NOT EXISTS `items_data`(
                id,
                month_count,
                sale_count_,
                favorite_count,
                order_date date
                )'''
        self.execute_db(items_info)
        self.execute_db(items_data)

    def insert_many(self, sql, values):
        '''执行插入多条记录SQL语句，values为插入值的列表或元组，为可迭代对象'''
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                c.executemany(sql,values)

    def select_db(self, sql, datas=None):
        '''执行查询类SQL语句,datas为占位符参数'''
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                if datas:
                    c.execute(sql, datas)
                else:
                    c.execute(sql)
                return c.fetchall()

    def execute_db(self, sql, datas=None):
        '''执行非查询类SQL语句，datas为占位符参数'''
        if sql is not None and sql != '':
            with self.conn:
                c = self.conn.cursor()
                if datas:
                    c.execute(sql, datas)
                else:
                    c.execute(sql)





if __name__ == "__main__":
    c = GoodTables()
    #c.run_once()
    #datas =(1,2,3,4,5)
    #sql = 'INSERT INTO items_data VALUES (?,?,?,?,?)'
    #c.execute_db(sql, datas)
    #sql_rm = "DELETE FROM items_data"
    #datas = ('商品ID4',)
    #c.execute_db(sql_rm)
    #sql = "SELECT * FROM items_data WHERE order_date like ?"
    #datas = (time.strftime("%Y-%m-%d")+'%',)
    #for item in c.select_db(sql, datas):
        #print(item)
    sql = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    result = c.select_db(sql)
    if result:
        for table_name in result:
            sql = "SELECT * FROM {}".format(table_name[0])
            print(table_name[0])
            for item in c.select_db(sql):
                print(item)
    else:
        c.run_once()

