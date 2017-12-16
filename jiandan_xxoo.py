#!/usr/bin/env python3
# encoding=utf-8
import time
import os
import sys
import argparse
import urllib.request
 
from bs4 import BeautifulSoup
from selenium import webdriver


def jdSpider(start, end):
    """
    煎蛋妹子图爬虫函数
    :param start: start page number
    :param end: end page number
    :return:
    """
    urls = ('http://jandan.net/ooxx/page-{}#comments'.format(i) for i in range(start, end+1))
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'

    driver = webdriver.Firefox()
    driver.maximize_window()

    x = 1

    # 存储图片的路径
    try:
        dirpath = './mm'
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
    except:
        print '创建目录异常'
        sys.exit(0)

    # 按页访问，获取所有mm图下载地址
    for url in urls:
        print("正在访问{}".format(url)) 
        try:
            driver.get(url)
            driver.implicitly_wait(10)
            data = driver.page_source
            soup = BeautifulSoup(data, 'lxml')
            hrefs = soup.find_all('a',class_="view_img_link")
        except:
            print("访问异常！")  
            continue

        print("开始下载") 
        for href in hrefs:
            img = href.get('href')
            img = "http:" + img
            print("正在下载第{}张图片".format(x))
            filename = os.path.join(dirpath, img.split('/')[-1])

            try:
                urllib.request.urlretrieve(img,filename)
                x = x+1
                # time.sleep(0.1)
            except:
                print("img 访问异常！wating 60s.")
                time.sleep(60)
                continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='为应对煎蛋网反爬虫策略，利用selenium模拟浏览器，自动下载煎蛋网妹子图到本地')
    parser.add_argument('--range', required=True, nargs=2, metavar=('start', 'end'), help='page to download: --range 1 10')
    args = parser.parse_args()

    start = int(args.range[0])
    end = int(args.range[1])
    jdSpider(start, end)