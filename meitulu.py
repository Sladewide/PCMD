import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import os
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
wz='http://www.meitulu.cn'
wz_load=requests.get(wz,headers=headers).text
bs=BeautifulSoup(wz_load,'lxml')
list=bs.find_all('a',{'target':'_blank','href':re.compile('/item/.*?\.html')})

#
for i in range(20):
    for l in list:
        url2=str(l['href'])[-9:-5]
        url1='http://www.meitulu.cn/item/'
        url=url1+url2
        other1='.html'
        URL=url+other1
        html1 = urllib.request.urlopen(URL).read().decode('utf-8')
        soup1 = BeautifulSoup(html1, features='lxml')


        # 取出标题，创造文件夹
        title = str(soup1.h1.string)
        os.makedirs('./%s' % title, exist_ok=True)
        # 取出页数
        pp=soup1.find_all('p')[2]
        for p in pp:
             times=int(str(p)[-3:-1])

        def save():
            soup=BeautifulSoup(html,features='lxml')
            A=soup.find_all('img',{'src':re.compile('http://image.meitulu.cn/d/file/bigpic/.*?\.jpg')})
            print('正在下载的是%s' % title)
            print('下载到第{}张图片...还有{}张待下载...'.format(i + 1,(times-int(i+1))))
            for a in A:
                IMAGE_URL=a['src']
                r = requests.get(IMAGE_URL, headers=headers)
                img_name = IMAGE_URL.split('/')[-1]
                with open('./%s/%s' % (title ,img_name), 'wb') as f:
                    f.write(r.content)
        for i in range(times):
            if i==0:
                html = requests.get(url + other1, headers=headers).text
                soup = BeautifulSoup(html, features='lxml')
                save()

            else:
                other2='_'+str(i+1)+other1
                html = requests.get(url + other2, headers=headers).text
                save()
        print('下载已完成{}/20'.format(i+1))
print('**********下载完成！！！！*********')

