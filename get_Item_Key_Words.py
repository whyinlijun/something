#!/usr/bin/env python3
#coding:utf-8

import json,re,datetime,time
import requests
import csv

'''
本程序爬取生意参谋的商品关键词分析数据
'''

def get_pararms(token,itemID,page,days=1,web_device='2'):
    pararms = {
        '_:': '{:.0f}'.format(time.time()*1000),
        'token':token,
        'device': web_device,
        'dateType': 'day',       #'recent' + str(days),
        'dateRange': '{}|{}'.format(get_date(days), get_date(days)),
        'itemId': itemID,
        'order': 'uv',
        'orderType': 'desc',
        'search': '',
        'searchType':'taobao',
        'currentPage': page,
    }
    return pararms

def data_reduction(datas,key_date,itemid,device):
    re_list=[]
    for item in datas:
        re_list.append({
            '关键词':item['keyword'],
            '浏览量':item['pv'],
            '访客数':item['uv'],
            '平均流览量':item['avgPv'],
            '跳出率':item['bounceRate']*100,
            '支付买家数':item['payBuyerCnt'],
            '支付件数':item['payItemQty'],
            '支付金额':item['payAmt'],
            '支付转化率':item['payRate']*100,
            '日期':key_date,
            '商品ID':itemid,
            '设备':'无线端' if device=='2' or device==2 else 'PC',
            '搜索排名':item.get('avgSeRank'),
            '曝光量':item.get('expose'),
            '点击量':item.get('clickCnt'),
            '点击率':item.get('clickRate')*100 if 'clickRate' in item else None
        })
    return re_list

def get_date(days):
    return (datetime.date.today() - datetime.timedelta(days)).strftime('%Y-%m-%d')

def sycm_good_data_get(params,headers):
    url='https://sycm.taobao.com/bda/items/itemanaly/itemformto/findItemKeywords.json'
    web_data=requests.get(url,headers=headers,params=params)
    return web_data.text

def save_csv(filename,dict_datas):
    with open(filename,'w',encoding='utf8') as csvfile:
        fieldname=['日期','设备','商品ID','关键词','搜索排名','曝光量', '点击量','点击率','浏览量','访客数','平均流览量','跳出率','支付买家数','支付件数', '支付金额','支付转化率']
        csv_write=csv.DictWriter(csvfile,fieldnames=fieldname)
        csv_write.writeheader()
        csv_write.writerows(dict_datas)
        #for item in dict_datas:
            #csv_write.writerow(item)

def get_google_head(h_str):
    token = re.findall('token=(.*?)&', h_str)[0]
    header = {}
    for item in h_str.split('\n')[1:]:
        # google浏览器请求头会有以：开始的，如果检测到就去掉
        item = item.strip(':')
        split_list = item.split(':', 1)
        header[split_list[0]] = split_list[1].strip()
    return token,header

def main(str1,itemid,days,device='2'):
    re_list=[]
    token,header=get_google_head(str1)
    while True:
        page=1
        while True:
            print("正在处理{}第{}页".format(get_date(days),page))
            pararms=get_pararms(token,itemid,page,days,device)
            web_data=sycm_good_data_get(pararms,header)
            json_data=json.loads(web_data)
            if 'data' in json_data:
                if len(json_data['data']['list'])>0:
                    re_list.extend(data_reduction(json_data['data']['list'], get_date(days), itemid, device))
                if json_data['data']['totalPage']>page:
                    page+=1
                    time.sleep(1)
                else:
                    break
            else:
                break
        days-=1
        time.sleep(5)
        if days==0:
            break
    return re_list

if __name__=='__main__':
    str1=''':authority:sycm.taobao.com
:method:GET
:path:/bda/items/itemanaly/itemformto/findItemKeywords.json?currentPage=8&dateRange=2018-04-21%7C2018-04-21&dateType=recent1&device=2&itemId=567069635897&order=uv&orderType=desc&search=&searchType=taobao&token=688fcf1b7&_=1524402431478
:scheme:https
accept:*/*
accept-encoding:gzip, deflate, br
accept-language:zh-CN,zh;q=0.9
cookie:t=616e3fb773d450d463bb8959f68692ad; cookie2=1ada09b05f4d6b0d1143e5dc74e0347f; cna=9XBjEzLm6AACATypkG6+ZTiU; JSESSIONID=0AC2B997FE8883AED44C650D4A17F27A; x=99778076; uc1=cookie14=UoTeOozfHbLHVw%3D%3D&lng=zh_CN; uc3=nk2=&id2=&lg2=; tracknick=; sn=liguirong91%3Ack; csg=7469e5f3; unb=2334152358; skt=513e031c318d0866; _euacm_ac_rs_sid_=35745462; v=0; _portal_version_=new; flow_version=new; _euacm_ac_l_uid_=2334152358; 2334152358_euacm_ac_c_uid_=99778076; 2334152358_euacm_ac_rs_uid_=99778076; enc=XvfthjcXElDtitct9H0zJs13L54jrCfjnwugUZ2ZrpCkbHzr0gHq7hCbe1bPcZ0uuhbn8r0QIgPsvifkbqAZZA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; _tb_token_=3e83d7803b5ee; mt=ci%3D-1_1; apush30c9ac7d03d7ab7fe36fa8da959ca8fc=%7B%22ts%22%3A1524402431201%2C%22parentId%22%3A1524401054463%7D; isg=BL-_UHUy2SqV1902w0mGyaYyTpqJDAyJc8Iy11GPMG6DYM_iWHCjl802pzCeBuu-
referer:https://sycm.taobao.com/bda/items/itemanaly/item_analy.htm?spm=a21ag.7634351.LeftMenu.d510.5cf2395fDsVMLp
user-agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'''
    itemid='567069635897'
    aisa_name = "碎花连衣裙"
    days=7
    device=2
    filename='/home/yinsir/'+aisa_name+'_'+itemid+'_最近'+str(days)+'天关键词效果分析.csv'
    datas=main(str1,itemid,days,device)
    save_csv(filename,datas)




