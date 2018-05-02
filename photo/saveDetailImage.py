#!/usr/bin/env python3
#coding:utf-8
'''
本程序抓取淘宝商品的详情页的标题图和详情图
输入网址，商品名称
目录可以更改
'''
import re,os,sys
import requests

def getUrl(url):
    try:
        content=requests.get(url).text
    except:
        print('网页读取出错')
        content=False
    return content

def get_good_image_url(web_data):
    image_list=[]
    re_compile=re.compile('auctionImages\s+:\s*\[(".*?")\]',re.S)
    g=re.search(re_compile,web_data).group(1)
    for i in g.split(','):
        image_list.append('http:'+i[1:-1])
    return image_list
    
def get_detail_image_url(web_data):
    re_compile=re.compile(r"location.protocol.*?,",re.S)
    url_compile=re.compile("\'(.*?)\'")
    g=re.search(re_compile,web_data)
    a=re.findall(url_compile,g.group())
    dec_images=getUrl(a[0]+a[1])
    #两个地址结果是一样的
    #desc_image=getUrl(a[0]+a[2])
    image_compile=re.compile('(https://[^\s]*[jpg|gif|jpeg|bmp|png])"',re.I)
    image_list=re.findall(image_compile,dec_images)
    return image_list

def make_dir(path,subdir):
    try:
        os.mkdir(path+'/'+subdir)
    except Exception as e:
        print(Exception,":",e)
    return
    
def save_image(path,image_name,image_list,flag='detail'):
    if flag!='detail':
        make_dir(path + '/' + image_name, 'head')
    image_xuhao=1
    ex_compile='(jpg|gif|jpeg|bmp|png)'
    for i in image_list:
        try:
            response=requests.get(i,stream=True)
            image=response.content
        except:
            print('Image NO.%s is ERROR!!!' %str(image_xuhao))
            image_xuhao+=1
            continue
        else:
            print('Image url:'+i)
            if re.search(ex_compile,i):
                ex_name=re.search(ex_compile,i).group(1)
            else:
                ex_name='jpg'
            strxuhao=str(image_xuhao) if image_xuhao>=10 else '0'+str(image_xuhao)
            if flag=='detail':
                imgfile=open(path+"/"+image_name+'/'+image_name+'_'+strxuhao+'.'+ex_name,'wb')
            else:
                imgfile=open(path+"/"+image_name+'/head/'+image_name+'_big_'+strxuhao+'.'+ex_name,'wb')
            imgfile.write(image)
            imgfile.close()
            print('Image NO.%s is download' %str(image_xuhao))
            image_xuhao+=1
    return

def save_html(filename,content):
    with open(filename,'w') as fs:
        fs.write(content)
    return

def save_main(url,image_name='default',flag='all'):
    web_data=getUrl(url)
    path="/home/yinsir/下载/淘宝图片"
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    make_dir(path,image_name)
    #判断保存哪一片图片
    if flag=="all":
        save_image(path,image_name,get_good_image_url( web_data),flag='nodetail')
        save_image(path,image_name,get_detail_image_url( web_data),flag='detail')
    elif flag=="detail":
        save_image(path,image_name,get_detail_image_url( web_data),flag='detail')
    else:
        save_image(path,image_name,get_good_image_url( web_data),flag='nodetail')
    return

    
if __name__=="__main__":

    id=input(u"请输入集市商品ID:")
    url="https://item.taobao.com/item.htm?id={}".format(id)
    dir_name=input(u'输入保存图片目录名称：')
    save_main(url,dir_name,'all')
