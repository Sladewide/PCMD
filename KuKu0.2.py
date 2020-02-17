import os,re,urllib.request,requests,time,concurrent
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
old='"+m201304d+"'
new='https://s2.kukudm.com/'
#找到漫画的每个章节
def bs():
    global x
    r = requests.get(x, headers=headers)
    r.encoding = ('gbk')
    bs=BeautifulSoup(r.text,'lxml')
    return bs
title=''
chapter_sites=[]
chapter_names=[]
names=[]
def all_chapters():#全下载
    global title, chapter_sites,names,bs
    title_false=bs().title.string
    title=re.split('漫画在线_在线漫画',title_false)[0]
    if not os.path.exists('./%s'%title):
        os.makedirs('./%s'%title)
    names=chapters_names().copy()
    #获取漫画标题
    chapters=bs().find_all('a',{'target':'_blank','href':
        re.compile('https://comic2.kukudm.com/comiclist/.*?.htm')})
    for chapter in chapters:
        chapter_sites.append(chapter['href'])
     #每章节地址

def select_chapter(temp):#选择性下载
    global title,chapter_sites,chapter_names,names
    title_false = bs().title.string
    title = re.split('漫画在线_在线漫画', title_false)[0]
    if not os.path.exists('./%s' % title):
        os.makedirs('./%s' % title)
    # 获取漫画标题
    chapters_names()
    list=chapters_names.copy()
    new=[l[len(title+' '):] for l in list]
    chapters = bs().find_all('a', {'target': '_blank', 'href':
        re.compile('https://comic2.kukudm.com/comiclist/.*?.htm')})
    for chapter in chapters:
        chapter_sites.append(chapter['href'])
    chapter_sites=chapter_sites[new.index(temp):]
    names=list[new.index(temp):]

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
def download(chapters_names):
    print('下载开始！！！')
    global chapter_sites,names
    time_start = time.time()
    for i in range(len(chapter_sites)):
        chapters_name=chapters_names[i]
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
            print('正在下载{}第{}页,还剩{}页'.format(chapters_name,i,int(pages(str(bs)))-i))
            with open('./%s/%s/%s' % (title,chapters_name,img_name[i-1]), 'wb') as f:
                f.write(r.content)
        process = round(i / len(chapter_sites), 2)
        print('本话内容下载完毕！')
    print('下载完成！！！')

def main():
    global x
    x=input('请输入漫画主页地址')
    choice=int(input('下载全部章节还是选择性下载？前者请输入0，后者请输入1'))
    if choice==0:
        bs()
        all_chapters()
        download(chapters_names=names)
    elif choice==1:
        bs()
        begin = input('从第几话开始下载')
        select_chapter(temp=begin)
        download(chapters_names=names)
main()
