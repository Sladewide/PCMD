
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
' 赛博朋克同人插画下载  '
 
__author__ = 'Sladewide'
import requests,os,bs4,re
url1 =
url2 = 'https://www.zcool.com.cn/work/ZMzkwNTg5MTY=.html'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
r=requests.get(url,headers=headers)
soup=bs4.BeautifulSoup(r.text,'lxml')
pic=soup.find_all('img',{'data-src':re.compile('https://img.zcool.cn/community/.*?.jpg')})
l=[p['data-src'] for p in pic]
for i in l:
    IMAGE_URL=i
    r = requests.get(IMAGE_URL, headers=headers)
    img_name = IMAGE_URL.split('/')[-1]
    with open('./%s/%s' % img_name, 'wb') as f:
        f.write(r.content)
print('下载完成！！！')
