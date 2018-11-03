#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

'''
抓取商品评论数据
有图片的
https://rate.taobao.com/feedRateList.htm?

auctionNumId=557946516364
currentPageNum=1
pageSize=20
rateType=3
orderType=sort_weight
folded=0
_ksTS=1524011554378_1459
callback=jsonp_tbcrate_reviews_list

ratetype 3 图片
         -1 差评
         0 中评
         1 好评
         2 追评
'''

import requests
import re , json , os ,time
import sqlite3

def get_comment(num_iid,rate_type=3):
    header = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    url = "https://rate.taobao.com/feedRateList.htm"
    page = 1
    re_com = re.compile('b_(.*?)\.gif')
    pic_url=[]
    video_url=[]
    while True:
        payload ={
            "auctionNumId":num_iid,
            "currentPageNum":page,
            "pageSize":20,
            "rateType":rate_type,
            "orderType":"sort_weight",
            "folded":0,
            #"_ksTS":"1524011554378_1459",
            "callback":"jsonp_tbcrate_reviews_list"
        }
        t = requests.get(url,params=payload,headers=header)
        c = re.search('\((.*)\)',t.text).group(1)
        if c:
           c = json.loads(c)
           for item in c['comments']:
               #print(item['user']['rank'],'----',item['user']['displayRatePic'],'----',item['user']['vipLevel'])
               ratepic = re.search(re_com,item['user']['displayRatePic'])
               print(item['buyAmount'],'\t',item['date'],'\t',item['dayAfterConfirm'],'\t',
                     '{:<8}'.format(item['user']['nick']),'\t',
                      '{:>3}'.format(item['user']['rank']),'\t',
                     item['user']['vipLevel'],'\t','{:<6}'.format(ratepic.group(1) if ratepic else 'red_0'),'\t',
                     item['tag'],item['lastModifyFrom'],'\t',item['content'])
               #评论中的图片
               if item['photos']:
                   for photo_url in item['photos']:
                       #pic_url.append(photo_url['url'])
                       pic_url.append([photo_url['url'],item['user']['nick']])
               #评论中的视频
               if item['video']:
                   video_url.append(item['video']['cloudVideoUrl'])
               #追评中的图片
               if item['append']:
                   if item['append']['photos']:
                       for photo_url in item['photos']:
                           pic_url.append([photo_url['url'], item['user']['nick']])
                           #pic_url.append(photo_url['url'])

        page += 1
        if page > c.get('maxPage'):
            print("总计:", c['total'])
            break

    return pic_url,video_url

def save_comment():
    conn = sqlite3.connect('pic.db')
    conn.execute("drop table pic")
    conn.execute(
        "create table if not exists pic (url VARCHAR(100) PRIMARY KEY , "
        "down TINYINT(1) DEFAULT False , "
        "type VARCHAR(10) DEFAULT 'image',"
        "nick VARCHAR(10))"
    )
    pic ,video = get_comment(557946516364)
    conn.executemany(
        "INSERT OR IGNORE INTO pic(url,nick) VALUES(?,?)",[('http:'+item[0].replace('_400x400.jpg',''),item[1]) for item in pic])
    #conn.execute("delete from pic")

    with open('image.html','w') as fs:
        for row in conn.execute("select url from pic order by nick"):
            fs.write("<image src='{}' >".format(row[0]))
    conn.commit()
    conn.close()

class GetComment:
    def __init__(self,num_iid,asia_name=2,rate_type=3):
        self.num_iid = num_iid
        self.asia_name = asia_name
        self.rate_type = rate_type
        self.pic_url = []
        self.video_url = []

    def getComment(self):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        }
        url = "https://rate.taobao.com/feedRateList.htm"
        page = 1
        re_com = re.compile('b_(.*?)\.gif')
        while True:
            payload = {
                "auctionNumId": self.num_iid,
                "currentPageNum": page,
                "pageSize": 20,
                "rateType": self.rate_type,
                "orderType": "sort_weight",
                "folded": 0,
                # "_ksTS":"1524011554378_1459",
                "callback": "jsonp_tbcrate_reviews_list"
            }
            t = requests.get(url, params=payload, headers=header)
            c = re.search('\((.*)\)', t.text).group(1)
            if c:
                c = json.loads(c)
                for item in c['comments']:
                    ratepic = re.search(re_com, item['user']['displayRatePic'])
                    print(item['buyAmount'], '\t', item['date'], '\t', item['dayAfterConfirm'], '\t',
                          '{:<8}'.format(item['user']['nick']), '\t',
                          '{:>3}'.format(item['user']['rank']), '\t',
                          item['user']['vipLevel'], '\t', '{:<6}'.format(ratepic.group(1) if ratepic else 'red_0'),
                          '\t',
                          item['tag'], item['lastModifyFrom'], '\t', item['content'])
                    # 评论中的图片
                    if item['photos']:
                        for photo_url in item['photos']:
                            # pic_url.append(photo_url['url'])
                            self.pic_url.append([photo_url['url'], item['user']['nick']])
                    # 评论中的视频
                    if item['video']:
                        self.video_url.append(item['video']['cloudVideoUrl'])
                    # 追评中的图片
                    if item['append']:
                        if item['append']['photos']:
                            for photo_url in item['photos']:
                                self.pic_url.append([photo_url['url'], item['user']['nick']])


            page += 1
            if page > c.get('maxPage'):
                print("总计:", c['total'])
                break

    def save_image(self,picpath):
        header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        }
        if self.pic_url:
            ex_compile = '(jpg|gif|jpeg|bmp|png)'
            try:
                os.mkdir(picpath)
            except Exception as e:
                print(e)
            image_xuhao = 1
            for url in self.pic_url:
                url = 'http:'+url[0][:-12]
                print(url)
                try:
                    response = requests.get(url,stream = True ,headers = header)
                    image = response.content
                except:
                    print('url ERROR!!!' % url)
                    image_xuhao += 1
                    continue
                else:
                    print('Image url:' + url)
                    if re.search(ex_compile, url):
                        ex_name = re.search(ex_compile, url).group(1)
                    else:
                        ex_name = 'jpg'
                    strxuhao = str(image_xuhao) if image_xuhao >= 10 else '0' + str(image_xuhao)
                    picname = picpath + '/' + strxuhao + '.' + ex_name
                    with open(picname,'wb') as fs:
                        fs.write(image)
                    image_xuhao += 1
                    time.sleep(3)




    def __call__(self):
        print(self.asia_name)

if __name__ == '__main__':
    good = GetComment(567069635897,'了')
    good.getComment()
    #print(good.pic_url)
    good.save_image('/home/luck/下载/碎花裙')
