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

# 生成网址列表
def buildUrls(word):
    word = urllib.parse.quote(word)
    #url = r"http://pic.sogou.com/pics?query={word}&mode=1&start={pn}&reqType=ajax&reqFrom=result&tn=0"
    url = r"http://cn.bing.com/images/async?q={word}&first={pn}&count=35&relp=35&lostate=r&mmasync=1&IG=BD3523DBD28B4DA0B59C6217F2C39790&SFX=3&iid=images.5727"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))
    return urls

# 解析JSON获取图片URL
#re_url = re.compile(r'"pic_url":"(.*?)"')
re_url = re.compile(r'http:[\w\/\.\-]*\.jpg')
def resolveImgUrl(html):
    #imgUrls = [decode(x) for x in re_url.findall(html)]
    print (type(html))
    imgUrls = re_url.findall(html)
    print (imgUrls)
    return imgUrls

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
    print("欢迎使用Bing图片下载脚本！\n目前仅支持单个关键词。")
    print("下载结果保存在脚本目录下的results文件夹中。")
    print("=" * 50)
    word = input("请输入你要下载的图片关键词：\n")

    dirpath = mkDir("results")

    urls = buildUrls(word)
    index = 0
    for url in urls:
        print("正在请求：", url)
        #html = requests.get(url, timeout=10).content.decode('utf-8')
        html = requests.get(url, timeout=10).text
        imgUrls = resolveImgUrl(html)
        if len(imgUrls) == 0:  # 没有图片则结束
            break
        for url in imgUrls:
            if downImg(url, dirpath, str(index) + ".jpg"):
                index += 1
                print("已下载 %s 张" % index)
