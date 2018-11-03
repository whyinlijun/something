#!/usr/bin/env python3
#coding:utf-8

'''
    商品效果明细,返回全部在售有访客商品数据
    https://sycm.taobao.com/bda/items/effect/getItemsEffectDetail.json?
    dateRange=2017-04-23%7C2017-04-23&
    dateType=day&
    device=0&
    orderDirection=false&
    orderField=clickRate&
    page=1&
    pageLimit=10&
    token=7b2a873eb&
    type=1&
    _=1493191080816
    数据结构：
                traceId
                code
                data
                    recordCount
                    data
                        0....n
                            'itemId',
                            'itemEffectIndex',
                                    addCartItemCnt----------------加购件数
                                    avgBounceUvRate---------------详情页跳出率
                                    avgStayTime-------------------平均停留时长
                                    clickCnt----------------------点击次数
                                    clickRate---------------------点击率
                                    expose------------------------曝光量
                                    favBuyerCnt-------------------收藏人数
                                    id----------------------------
                                    itemPv------------------------商品浏览量
                                    itemUv------------------------商品访客数
                                    orderAmt----------------------下单金额
                                    orderBuyerCnt-----------------下单买家数
                                    orderItemQty------------------下单件数
                                    orderRate---------------------下单转化率
                                    orderToPayRate----------------下单支付转化率
                                    payAmt------------------------支付金额
                                    payBuyerCnt-------------------支付买家数
                                    payBuyerCntSe-----------------搜索引导支付买家数
                                    payItemQty--------------------支付件数
                                    payPct------------------------客单价
                                    payRate-----------------------支付转化率
                                    rfdSucAmt---------------------售中售后成功退款金额
                                    rfdSucCnt---------------------售中售后成功退款笔数
                                    sePayRate---------------------搜索支付转化率
                                    uvAvgPayAmt-------------------访客平均价值
                                    uvSe--------------------------搜索引导访客数
                            'itemModel'
                                    'title',
                                    'isWirelessPublished',
                                    'quantity',
                                    'categoryId',
                                    'mallItem',
                                    'itemStatus',
                                    'itemDetailUrl',
                                    'reservePrice',
                                    'pictUrl',
                                    'publishTime',
                                    'id'
                message

'''
import time
from sycm_getPublic import *
import sycm_config

def data_sorting(data,itemDate,deviceName):
    reduction={
        '加购件数': data['addCartItemCnt'],
        '详情页跳出率': round(data['avgBounceUvRate']*100,2),
        '平均停留时长': data['avgStayTime'],
        '点击次数': data['clickCnt'],
        '点击率': round(data['clickRate']*100,2),
        '曝光量': data['expose'],
        '收藏人数': data['favBuyerCnt'],
        '商品ID': data['id'],
        '商品浏览量': data['itemPv'],
        '商品访客数': data['itemUv'],
        '下单金额': data['orderAmt'],
        '下单买家数': data['orderBuyerCnt'],
        '下单件数': data['orderItemQty'],
        '下单转化率': round(data['orderRate']*100,2),
        '下单支付转化率': round(data['orderToPayRate']*100,2),
        '支付金额': data['payAmt'],
        '支付买家数': data['payBuyerCnt'],
        '搜索引导支付买家数': data['payBuyerCntSe'],
        '支付件数': data['payItemQty'],
        '客单价': data['payPct'],
        '支付转化率': round(data['payRate']*100,2),
        '售中售后成功退款金额': data['rfdSucAmt'],
        '售中售后成功退款笔数': data['rfdSucCnt'],
        '搜索支付转化率': round(data['sePayRate']*100,2),
        '访客平均价值': data['uvAvgPayAmt'],
        '搜索引导访客数': data['uvSe'],
        '日期':itemDate,
        '设备':deviceName
    }
    return reduction

def get_pararms(token,days=1,web_device='2'):
    if  web_device not in ('0','1','2',0,1,2) or not token:
        return None
    pararms = {
        '_:': '{:.0f}'.format(time.time()*1000),
        'token':token,
        'device': web_device,
        'dateType': 'day',       #'recent' + str(days),
        'dateRange': '{}|{}'.format(get_date(days), get_date(days)),
        'orderDirection':'false',
        'orderField' : 'itemPv',
        'page' :'1' ,
        'pageLimit':'10',
        'type':'0',
    }
    return pararms

def main(days=1,device=2):
    sort_datas=[]
    url = 'https://sycm.taobao.com/bda/items/effect/getItemsEffectDetail.json?'
    token,header=get_google_head(sycm_config.headerString)
    deviceName=get_device_name(device)
    while True:
        pararms=get_pararms(token,days,device)
        json_data=get_web_to_json(url,pararms,header)
        for item in json_data.get('data').get('data'):
            sort_data=data_sorting(item.get('itemEffectIndex'),get_date(days),deviceName)
            dictPrint(sort_data)
            sort_datas.append(sort_data)
        days-=1
        if days==0:
            break
    return sort_datas


if __name__=='__main__':
    main()


