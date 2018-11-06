#! /usr/bin/env python3
#coding : utf-8

'''
本库为sqlite3操作数据库

'''

import os, sqlite3, time

DB_FILE_PATH = 'd://test.db'
SHOW_SQL = True

def get_conn(path=""):
    if path != '':
        print('{}在硬盘上'.format(path))
        conn = sqlite3.connect(path)
    else:
        print('在内存上')
        conn = sqlite3.connect(":memory:")
    return conn

def create_sql(conn, sql):
    if sql is not None and sql != '':
        with conn:
            c = conn.cursor()
            c.execute(sql)
            if SHOW_SQL:
                print('执行sql: [{}]'.format(sql))
            conn.commit()
    else:
        print("[{}] is empty or equal is None!".format(sql))


def insert_order(conn, sql, values):
    if sql is not None and sql != '':
        with conn:
            c = conn.cursor()
            c.executemany(sql,values)
            conn.commit()

def select_sql(conn, sql):
    if sql is not None and sql != '':
        with conn:
            c = conn.cursor()
            c.execute(sql)
            return c.fetchone()


def init(conn):
    create_sql_items = '''CREATE TABLE  IF NOT EXISTS `items` ( 
        `id` varchar(20) PRIMARY KEY,
        `title` varchar(40),
        `sell_id` varchar(20),
        `category` varchar(20),
        `url` varchar(100),
        `pic` varchar(100),
        `price` float,
        `promo_price` float,
        `month_count` int,
        `sale_count` int,
        `favorite` int
        )'''
    create_sql(conn,create_sql_items)
    create_sql_count_items = ''' CREATE TABLE IF NOT EXISTS `count_items`(
        id, month_count, sale_count_,favorite_count,order_date
        )'''
    create_sql(conn, create_sql_count_items)


def main():
    zhan_wei_fu = ','.join(['?' for item in range(11)])
    insert_sql = "INSERT INTO `items` VALUES({})".format(zhan_wei_fu)
    values = [('558470001549',
              '新款中老年羽绒马甲男士大码秋冬季羽绒背心加厚保暖坎肩马夹内胆',
              '839762818',
              '50011153',
              'http://item.taobao.com/item.htm?scm=1007.11502.21311.100200300000003&id=558470001549&pvid=9728a94a-d8de-4899-aba6-3407d406b502',
              'http://img.alicdn.com/bao/uploaded/i1/839762818/TB22grDXamgSKJjSsphXXcy1VXa_!!839762818.jpg',
              198.0,
              198.0,
              3222,
              35917,
              21916),]
    conn = get_conn(DB_FILE_PATH)
    insert_order(conn, insert_sql, values)
    #init(conn)

if __name__ == "__main__":
    sql = "SELECT * FROM count_items WHERE id = {} AND order_date = '{}'".format('558470001549', time.strftime("%Y-%m-%d"))
    print(sql)
    conn = get_conn(DB_FILE_PATH)
    print(select_sql(conn,sql))

