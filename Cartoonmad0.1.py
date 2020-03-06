import requests,time,os,re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
url='https://www.cartoonmad.com/comic/4855.html'
s=url.split('/')[-1]
pantern='/comic/'+s[:-5]+'.html'
r=requests.get(url,headers=headers)
r.encoding='Big5'
bs=BeautifulSoup(r.text,'lxml')
A=bs.find_all('a',{'href':pantern})
Manga_name=[a.string for a in A][-1]
B=bs.find_all('a',{'target':'_blank','href':re.compile('/comic/.*?.html')})
chapters_name=[b.string for b in B]
chapters_list=['https://www.cartoonmad.com'+ b['href'] for b in B]
dict=dict(zip(chapters_list,chapters_name))
def pages_number(url_lsit):
    global headers
    r = requests.get(url_lsit, headers=headers)
    r.encoding = 'Big5'
    bs = BeautifulSoup(r.text, 'lxml')
    time=bs.find_all('option',{'value':re.compile('.*?.html')})
    return len(time)

def donwload(url_lsit,chapter,url_name,image_site):
    #https://www.cartoonmad.com/comic/4855.html
    #https://www.cartoonmad.com/75550/4855/
    global headers,Manga_name
    if os.path.exists('./%s/%s'%(Manga_name,url_name)) == False:
        os.makedirs('./%s/%s' % (Manga_name,url_name))
    for i in range(pages_number(url_lsit)):
        n = ('%03d' % int(i + 1))
        url = image_site + chapter +  '/'+ n + '.jpg'
        print(url)
        r = requests.get(url, headers=headers)
        name = n + ".jpg"
        with open('./%s/%s/%s' %(Manga_name,url_name,name), 'wb') as f:
            f.write(r.content)
if __name__ == '__main__':
    executor = ThreadPoolExecutor(max_workers=5)
    image_site = 'https://www.cartoonmad.com/75550/4855/'
    n=0
    for d in dict:
        n+=1
        chapter=('%03d' % n)
        url_list=d
        url_name=dict[d]
        executor.submit(donwload,url_list,chapter,url_name,image_site)
