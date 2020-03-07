import requests,time,os,re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
'''
可能存在的bug：
直接输入图源id可能地址不对,就需要输入完全
若漫画名末尾有？！。这些特殊符号，可能导致路径设置失效
'''
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
print('欢迎使用cartoon漫画下载小工具\n仅支持https://www.cartoonmad.com/')
temp=input('请输入下载漫画主页id-----')
image_site =input('请输入图片地址id或者全地址\n例如https://www.cartoonmad.com/75550/4855/或75550\n')
if image_site[0]=='h':
    pass
else:
    image_site='https://www.cartoonmad.com/'+image_site+'/'+temp+'/'
url='https://www.cartoonmad.com/comic/'+temp+'.html'
print('-----------------华丽的分割线--------------------\n解析中....')
s=url.split('/')[-1]
pantern='/comic/'+s[:-5]+'.html'
r=requests.get(url,headers=headers)
r.encoding='Big5'
bs=BeautifulSoup(r.text,'lxml')
A=bs.find_all('a',{'href':pantern})
Manga_name=[a.string for a in A][-1]
if Manga_name[-1]=='?':
    Manga_name=Manga_name[:-1]
B=bs.find_all('a',{'target':'_blank','href':re.compile('/comic/.*?.html')})
chapters_name=[b.string for b in B]
chapters_list=['https://www.cartoonmad.com'+ b['href'] for b in B]
Dict=dict(zip(chapters_list,chapters_name))
print('<<{}>>总共有{}话'.format(Manga_name,len(Dict)))

#直接在主页获取每话页数
l=[]
def pages_number():
    global bs,l
    N1=bs.find_all('font',{'style':'font-size:8pt;color: #888888;'})
    N2=[n.string for n in N1]
    for n in N2:
        a=re.compile('\d+').findall(str(n))
        l=l+a
    return l
pages_number()
def donwload(url_lsit,chapter,url_name,image_site,n):
    global headers,Manga_name,l
    if not os.path.exists('./%s/%s' % (Manga_name, url_name)):
        os.makedirs('./%s/%s' % (Manga_name,url_name))
    for i in range(int(l[n-1])):
        n = ('%03d' % int(i + 1))
        url = image_site + chapter + '/'+ n + '.jpg'
        print(url)
        print('正在下载%s%s第%s张图片' %(Manga_name,url_name,n))
        r = requests.get(url, headers=headers)
        name = n + ".jpg"
        with open('./%s/%s/%s' %(Manga_name,url_name,name), 'wb') as f:
            f.write(r.content)
    print('---------%s下载成功-------！'%url_name)

choice=input('全下载还是选择性下载，前者选0，后者为1----')
if choice=='1':
    x=input('从第几话开始下载(纯数字)---')
    x=('%03d'% int(x))
    search='第 '+ str(x) + ' 話'
    copy=chapters_name.copy()
    chapters_list=chapters_list[copy.index(search):]
    chapters_name=chapters_name[copy.index(search):]
    del Dict
    Dict = dict(zip(chapters_list,chapters_name))
    n=int(copy.index(search)) 
else:
    n=0
    pass
if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=5)
    for D in Dict:
        n += 1
        chapter=('%03d' % n)
        url_list=D
        url_name=Dict[D]
        executor.submit(donwload,url_list,chapter,url_name,image_site,n)
