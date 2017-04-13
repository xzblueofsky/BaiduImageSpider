#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: loveNight

import json
import itertools
import urllib
import requests
import os
import re
import sys

# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    #url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    url = r"http://pic.sogou.com/pics?query=test&mode=1&start=240&reqType=ajax&reqFrom=result&tn=0"
    urls = (url)
    #urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

def downImg(imgUrl, dirpath, imgName):
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(imgUrl, timeout=15)
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
    print("欢迎使用百度图片下载脚本！\n目前仅支持单个关键词。")
    print("下载结果保存在脚本目录下的results文件夹中。")
    print("=" * 50)
    word = input("请输入你要下载的图片关键词：\n")

    dirpath = mkDir("results")

    urls = buildUrls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)
        #html = requests.get(url, timeout=10).content.decode('utf-8')
        html = requests.get(url, timeout=10).content
        html = html.rstrip()
        html = html.replace("\r\n", "")
        print (html)
        requ_str = json.load(html, "ISO-8859-1")
        print (requ_str)
        #html = html.decode('utf-8') 
        #html = requests.get(url, timeout=10).content
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)

