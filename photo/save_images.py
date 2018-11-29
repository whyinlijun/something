#!/usr/bin/env python3
# _*_ coding : utf-8 _*_

'''
@author: Luke Yin
@contact: whyinlijun@gmail.com
@file: save_images.py
@time: 2018/11/5 13:18
@desc:
'''

import re, json, os, requests

class SaveGoodsImages():
    list_images = []
    property_images = []
    pc_detail_images =[]
    m_detail_images = []
    video_url =[]
    print_switch = True

    def __init__(self, path, num_id, goods_name):
        self.path = os.path.join(path, goods_name)
        self.num_id = num_id
        self.goods_name = goods_name
        self.goods_url = "https://item.taobao.com/item.htm?id={}".format(num_id)

    def getPcImages(self):
        try:
            content = requests.get(self.goods_url).text
        except:
            print('网页读取出错')
            content = False
        if content:
            #首图图片
            re_compile = re.compile('auctionImages\s+:\s*\[(".*?")\]', re.S)
            g = re.search(re_compile, content).group(1)
            for i in g.split(','):
                if 'http' not in i:
                    self.list_images.append('https:' + i[1:-1])
                else:
                    self.list_images.append( i[1:-1])
            #分类图片
            re_compile = re.compile('background:url\((.*)\)')
            f = re.findall(re_compile, content)
            if f:
                self.property_images = ['http:' + url[:-10] for url in f]
            #PC详情页图片
            re_compile = re.compile(r"location.protocol.*?,", re.S)
            url_compile = re.compile("\'(.*?)\'")
            g = re.search(re_compile, content)
            a = re.findall(url_compile, g.group())
            dec_images = requests.get(a[0] + a[1]).text
            image_compile = re.compile('(https://[^\s]*[jpg|gif|jpeg|bmp|png])"', re.I)
            self.pc_detail_images = re.findall(image_compile, dec_images)

    def get_m_dtail_images(self):
        url = 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdesc/6.0/'
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "referer": "https: // h5.m.taobao.com / app / detail / desc.html?_isH5Des = true"
        }
        params = {
            'data': '{"id":"' + self.num_id + '","type":"0", "f":"TB1MZOkhH2pK1RjSZFs8quNlXla"}',
        }
        re_compile = re.compile(r'\>(.*)\<')
        web = requests.get(url=url, params=params, headers=headers)
        data = json.loads(web.text)
        for image in data['data']['wdescContent']['pages']:
            i_url = re.search(re_compile, image)[1]
            if 'http' not in i_url:
                self.m_detail_images.append('https:' + i_url )
            else:
                self.m_detail_images.append(i_url)

    def get_video(self):
        url = "http://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/"
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
        }
        payload = {
            'callback': 'mtopjsonp1',
            'data': '{"itemNumId":"' + str(self.num_id) + '"}',
        }
        w = requests.get(url, headers=headers, params=payload).text
        w_re = re.search("\((.*)\)", w)
        if w_re:
            data = json.loads(w_re.group(1))['data']
            aa = json.loads(data['apiStack'][0]['value'])
            if aa['item'].get('videos'):
                self.video_url = aa['item']['videos'][0]['url']

    def save_video(self):
        if self.video_url:
            url = re.search('(.*?)\?', self.video_url).group(1)
            self.save_image(url, self.path, self.goods_name)



    def save_image(self, url, path, image_name):
        extensions = '\.(jpg|gif|jpeg|bmp|png|mp4|mpeg|avi)'
        extension = re.search(extensions, url).group(1) if re.search(extensions, url) else 'no_ext'
        file_name = os.path.join(path, image_name + '.' + extension)
        try:
            with open(file_name, 'wb') as fs:
                fs.write(requests.get(url, stream=True).content)
                if self.print_switch:
                    print('{} is download'.format(file_name))
        except:
            print(url,'   is not download')

    def save_images(self, sub_path, images_url):
        path = os.path.join(self.path, sub_path)
        if not os.path.exists(path):
            os.makedirs(path)
        image_xuhao = 1
        for image_url in images_url:
            str_xuhao = str(image_xuhao) if image_xuhao > 9 else '0' + str(image_xuhao)
            image_name = self.goods_name + '_' + str_xuhao
            self.save_image(image_url, path, image_name)
            image_xuhao += 1

if __name__ == "__main__":
    num_id = input('输入商品数字ID: ')
    asia_name = input('输入商品别名:')
    sm = SaveGoodsImages("D://淘宝图片", num_id, asia_name)
    sm.get_m_dtail_images()
    sm.getPcImages()
    sm.save_images('首图', sm.list_images)
    sm.save_images('颜色图', sm.property_images)
    sm.save_images('PC详情', sm.pc_detail_images)
    sm.save_images('无线详情', sm.m_detail_images)
    sm.get_video()
    sm.save_video()




