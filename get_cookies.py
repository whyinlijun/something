#! /usr/bin/env python3
#coding : utf-8

import time
from selenium import webdriver
from pyvirtualdisplay import Display


#url = 'https://sycm.taobao.com/custom/login.htm'
url = 'https://login.taobao.com/member/login.jhtml?from=sycm&full_redirect=true&style=minisimple&minititle=&minipara=0,0,0&sub=true&redirect_url=//sycm.taobao.com/custom/switch_redirect.htm'

display = Display(visible=1, size=(1600, 902))
display.start()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery");
chrome_options.add_argument("--start-maximized")

slf = webdriver.Chrome('../chromedriver', chrome_options=chrome_options)
#slf = webdriver.Firefox(executable_path='../geckodriver')
slf.delete_all_cookies()
slf.set_window_size(1024,800)
slf.set_window_position(0,0)
print('arguments done')
slf.get(url)
time.sleep(5)
slf.find_element_by_id('TPL_username_1').click()
slf.find_element_by_id('TPL_username_1').send_keys('左右逢源服饰')
slf.find_element_by_id('TPL_password_1').click()
slf.find_element_by_id('TPL_password_1').send_keys('zyou@yy810607')
#slf.find_element_by_id('J_SubmitStatic').click()

while True:
    if slf.current_url == 'https://sycm.taobao.com/portal/home.htm':
        print('check the page jump')
        slf.get(slf.current_url)
        time.sleep(3)
        break
    else:
        time.sleep(2)
