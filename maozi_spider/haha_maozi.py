#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
}

# 生成网址列表
def buildUrls():
    url = r"http://www.emaozi.com/goods-{pn}.html"
    urls = (url.format(pn=x) for x in range(1,10000))
    return urls

# 解析JSON获取图片URL
#re_url = re.compile(r'http:[\w\/\.\-]*\.jpg')
re_url = re.compile(r'\/images[\w\/\.\-]*\.jpg')
def resolveImgUrl(html):
    #print (type(html))
    #print (html)
    imgUrls = re_url.findall(html)
    for i in range(0,len(imgUrls)):
        imgUrls[i] = 'http://www.emaozi.com' + imgUrls[i]
    print (imgUrls)
    return imgUrls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        #res = requests.get(imgUrl, timeout=15)
        res = session.get(imgUrl, timeout=15)
        if str(res.status_code)[0] == "4":
            print(str(res.status_code), ":" , imgUrl)
            return False
    except Exception as e:
        print("抛出异常：", imgUrl)
        print(e)
        return False
    with open(filename, "wb") as f:
        f.write(res.content)
    return True


def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath

if __name__ == '__main__':

    dirpath = mkDir("results")

    urls = buildUrls()
    index = 0
    for url in urls:
        session = requests.Session()
        session.headers = headers
        print("正在请求：", url)
        #html = requests.get(url, timeout=10).content.decode('utf-8')
        #html = requests.get(url, timeout=10).text
        html = session.get(url, timeout = 15).text
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)
