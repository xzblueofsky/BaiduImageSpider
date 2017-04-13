#s!/usr/bin/env python3

import requests
import re
import os

#url = r'http://pic.sogou.com/pics?query=%B4%F7%C3%B1%D7%D3&w=05009900&p=40030500&_asf=pic.sogou.com&_ast=1491966326&sc=index&sut=3992&sst0=1491966326194'

url = r'http://cn.bing.com/images/search?q=%E6%88%B4%E5%B8%BD%E5%AD%90&go=Search&qs=n&form=QBILPG&sp=-1&pq=%E6%88%B4%E5%B8%BD%E5%AD%90&sc=8-3&sk=&cvid=FC5AF9B15E61432BB643D4C9273D5F02'

dirpath = r'img'

html = requests.get(url).text
#urls = re.findall(r'"pic_url":"(.*?)"', html)
#urls = re.findall(r'http:.*?\.jpg', html)
urls = re.findall(r'http:[\w\/\.\-]*\.jpg', html)

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
