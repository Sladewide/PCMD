import os,re,urllib.request,random,requests
from bs4 import BeautifulSoup
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
old='"+m201304d+"'
new='https://s2.kukudm.com/'
# x=input('请输入下载漫画的主页')
#找到漫画的每个章节
def bs():
    x = 'http://comic2.kukudm.com/comiclist/2964/index.htm'  # 测试网址
    r = requests.get(x, headers=headers)
    r.encoding = ('gbk')
    bs=BeautifulSoup(r.text,'lxml')
    return bs
title=''
chapter_sites=[]
chapter_names=[]
def all_chapters():#全下载
    global title, chapter_sites,chapter_names
    title_false=bs().title.string
    title=re.split('漫画在线_在线漫画',title_false)[0]
    if not os.path.exists('./%s'%title):
        os.makedirs('./%s'%title)
    #获取漫画标题
    chapters=bs().find_all('a',{'target':'_blank','href':
        re.compile('https://comic2.kukudm.com/comiclist/.*?.htm')})
    for chapter in chapters:
        chapter_sites.append(chapter['href'])
     #每章节地址


def chapters_names():
    global chapters_names
    chapters_name = bs().find_all('a', {'target': '_blank', 'href': re.compile('comiclist.*?.htm')})
    patern = re.compile('" target="_blank">(.+?)</a>')
    chapters_names = patern.findall(str(chapters_name))
    chapters_names = [x for x in chapters_names if x != '①' and x != '②' and x != '③']
    return chapters_names
    # 获取每章节名目录

#进入每话后的下载
def pages(r):
    patern=re.compile('共(\d+)页')
    pages=patern.findall(r)[0]
    return pages
    
def img_url(page):
    html = requests.get(page, headers=headers)
    html.encoding = 'gbk'
    bs = BeautifulSoup(html.text, 'xml')
    a=bs.find_all('IMG',{'SRC':True})
    b=re.split('[=\'>]',str(a))
    img_url=b[2].replace(old,new)
    return img_url
    
def download(chapter_sites):
    for i in range(len(chapter_sites)):
        chapters_name=chapters_names()[i]
        chapter_site=chapter_sites[i]
        html=requests.get(chapter_site,headers=headers)
        html.encoding='gbk'
        bs=BeautifulSoup(html.text,'xml')
        chapter_site1=chapter_site[:-5]
        if not os.path.exists('./%s/%s'%(title,chapters_name)):
            os.makedirs('./%s/%s'%(title,chapters_name))
        for i in range(1, int(pages(str(bs)))+1):
            page=chapter_site1+str(i)+'.htm'
            r = requests.get(img_url(page), headers=headers)        #最终图片源码
            img_name = [(str(i).rjust(3, '0')+'.jpg') for i in range(1,int(pages(str(bs)))+1)]
            # img_name1 = img_url(page).split('/')[-1]   #图片命名
            # img_name2=img_name2[].replace('')
            with open('./%s/%s/%s' % (title,chapters_name,img_name[i-1]), 'wb') as f:
                f.write(r.content)
bs()
all_chapters()
download(chapter_sites=chapter_sites)




