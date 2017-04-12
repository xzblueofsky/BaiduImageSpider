#s!/usr/bin/env python

import requests
import re
import os

#url = r'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=detail&fr=&sf=1&fmq=1447473655189_R&pv=&ic=0&nc=1&z=&se=&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E9%95%BF%E8%80%85%E8%9B%A4'
#url = r'http://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1491965833638_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E6%88%B4%E5%B8%BD%E5%AD%90'
url = r'http://pic.sogou.com/pics?query=%B4%F7%C3%B1%D7%D3&w=05009900&p=40030500&_asf=pic.sogou.com&_ast=1491966326&sc=index&sut=3992&sst0=1491966326194'

dirpath = r'img'

html = requests.get(url).text
urls = re.findall(r'"pic_url":"(.*?)"', html)

if not os.path.isdir(dirpath):
    os.mkdir(dirpath)

index = 1
for url in urls:
    print("Downloading:", url)
    try:
        res = requests.get(url)
        if str(res.status_code)[0] == "4":
            print("failed:", url)
            continue
    except Exception as e:
        print("failed:", url)
    filename = os.path.join(dirpath, str(index) + ".jpg")
    with open(filename, 'wb') as f:
        f.write(res.content)
        index += 1

print("%s pics downloades\n" % index)
