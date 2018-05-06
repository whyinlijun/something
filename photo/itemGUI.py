#!/usr/bin/env python3
#coding:utf-8

from tkinter import *
import tkinter.filedialog
import saveDetailImage as saveimage
import imagePJ as pj
import os


root=tkinter.Tk()
root.title('itemGUI')
save_directory=StringVar()
save_numid = StringVar()
save_title = StringVar()
save_directory.set('/home/yinsir')

def get_directory_name():
    save_directory.set(tkinter.filedialog.askdirectory(initialdir='/home/yinsir/harddisk/taobao_image'))
    return

def get_file_name():
    return tkinter.filedialog.askopenfile()

def getimage():
    print('getimage')
    id = save_numid.get()
    url = "https://item.taobao.com/item.htm?id={}".format(id)
    dir_name = save_directory.get()
    saveimage.save_main(url, save_title.get(), 'all',dir_name)

def pjimage():
    pic_path=save_directory.get()
    imagefiles = pj.getImageFile(pic_path)
    pj.imagePJ(imagefiles,pic_path)

def replace_image():
    result = pj.replace_pic_address(save_directory.get(), image_urls.get())
    if result:
        with open(os.path.join(save_directory.get(), 'replace.html'), 'w') as fs:
            fs.write(result.group())

fram1=Frame(root,padx=5,pady=5)
fram1.grid(row=0,)

fram2=Frame(root)
fram2.grid(row=1)


Label(fram1,text='商品ID:').grid(row=1,column=0,padx=10)
num_id=Entry(fram1 , textvariable = save_numid)
num_id.grid(row=1,column=1,padx=10,columnspan=2,sticky=E)
Label(fram1,text='商品命名:').grid(row=2,column=0,padx=10,pady=10)
num_name=Entry(fram1,textvariable=save_title)
num_name.grid(row=2,column=1,padx=10,columnspan=2,sticky=E)
Label(fram1,text='目录位置:').grid(row=0,column=0,padx=10,pady=10)
dir_label=Entry(fram1,textvariable=save_directory,width=15,state='readonly')
dir_label.grid(row=0,column=1)
Button(fram1,text='浏览',command=get_directory_name).grid(row=0,column=2,sticky=E,padx=10)
Label(fram1,text='图片地址:').grid(row=3,column=0)
image_urls=Entry(fram1)
image_urls.grid(row=3,column=1,columnspan=2,)

Button(fram2,text='获取图片',command=getimage).grid(row=0,column=0,padx=10,pady=5)
Button(fram2,text='拼接图片',command=pjimage).grid(row=0,column=1,padx=10,pady=5)
Button(fram2,text='地址替换',command=replace_image).grid(row=0,column=2,padx=10,pady=5)
root.mainloop()