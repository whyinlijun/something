#!/usr/bin/env python3
#coding:utf-8
'''
    本程序将某一目录下的图片，按图片名称排序拼接在一起！
    可以将切好的图片链接替换成网络图片地址
'''
import os,re
from PIL import Image
'''
im=Image.open('red.jpg')
print(im.mode,im.size,im.format)
im1=Image.open('green.jpg')
print(im.mode,im.size)
#im.show() 展示图片
#newImg = Image.new("RGBA",(640,480),(0,255,0)) #“RGBA”为图片的mode，（640，480）为图片尺寸，(0,255,0)为图片颜色，颜色第四位为alpha值，可填可不填
#newImg.save('out.png','PNG') #后面的png不写也可以，直接按照文件名的后缀.png存为相应格式了
#small_im=im.resize((400,400),Image.ANTIALIAS) #Image.ANTIALIAS 为抗锯齿
#im.paste(im1,(0,400))
#im.show()
'''

def imagePJ(imagelist,save_path):
    width=0
    height=0
    for item in imagelist:
        im=Image.open(item)
        width=im.size[0] if im.size[0]>width else width
        height+=im.size[1]
    new_image=Image.new('RGB',(width,height))
    weizhi=0
    for item in imagelist:
        im=Image.open(item)
        new_image.paste(im,(0,weizhi))
        weizhi+=im.size[1]
    new_image.save(os.path.join(save_path,'pj.jpg'),'JPEG')

def getImageFile(fspath):
    imagefiles=[]
    for item in os.listdir(fspath):
        if re.search('jpg|jpeg|png',item):
            imagefiles.append(os.path.join(fspath,item))
    return imagefiles

def replace_pic_address(path,replce_str):
    with open(os.path.join(path,'pj.html')) as fs:
        content=fs.read()
        souce_list=re.findall(r'src="(.*?)"',content,re.MULTILINE)
        replace_list=replce_str.split('\n')
        if len(souce_list)==len(replace_list):
            for s,r in zip(souce_list,replace_list):
                content=content.replace(s,r)
        else:
            print("数量不一致")
            return None
        return re.search(r'''<table.*?</table>''',content,re.S)






if __name__=="__main__":
    pic_path='d:\\淘宝抓图\\1735'
    #imagefiles=getImageFile(pic_path)
    #imagePJ(imagefiles,pic_path)

    replce_str='''https://img.alicdn.com/imgextra/i2/348151420/TB2vkNBnUhnpuFjSZFpXXcpuXXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2w5BlnSVmpuFjSZFFXXcZApXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i3/348151420/TB2_LlPnOlnpuFjSZFgXXbi7FXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2jJ4MnORnpuFjSZFCXXX2DXXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i2/348151420/TB21h8YnSFmpuFjSZFrXXayOXXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i4/348151420/TB2ly2vietTMeFjSZFOXXaTiVXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i4/348151420/TB2wwXTnS0mpuFjSZPiXXbssVXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2xr5HlwRkpuFjy1zeXXc.6FXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i4/348151420/TB2CQ53lrFkpuFjy1XcXXclapXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2_2VQnHlmpuFjSZFlXXbdQXXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i4/348151420/TB2G.OanNlmpuFjSZPfXXc9iXXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2m.yJlC0jpuFjy0FlXXc0bpXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i2/348151420/TB29EaolB0lpuFjSszdXXcdxFXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2h2aglChlpuFjSspkXXa1ApXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i2/348151420/TB2j.KelrBkpuFjy1zkXXbSpFXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2jlqOlrVkpuFjSspcXXbSMVXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i1/348151420/TB2hEQzincCL1FjSZFPXXXZgpXa_!!348151420.jpg
https://img.alicdn.com/imgextra/i3/348151420/TB2Q5V9nHBmpuFjSZFAXXaQ0pXa_!!348151420.jpg'''
    result=replace_pic_address(pic_path,replce_str)
    if result:
        with open(os.path.join(pic_path,'replace.html'),'w') as fs:
            fs.write(result.group())






