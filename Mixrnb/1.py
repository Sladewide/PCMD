import requests
r=requests.get('www.baidu.com').text
print(r)