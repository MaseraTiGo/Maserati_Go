#For get sed&pic
#fileauthor:Maser
#date:2016-12-20;20:14
import requests
from bs4 import BeautifulSoup
#the enter gate
sourceurl='http://100av.co/'
resone=requests.get(sourceurl)
resone.encoding='utf-8'
bsone=BeautifulSoup(resone.text,'html.parser')
#get all kinds of yellow url
lstone=bsone.select('a')
urlsone=[]
for lst in lstone:
    if lst.has_attr('href') and '/list/' in lst['href']:
       urlsone.append(sourceurl.rstrip('/')+lst['href'])
print(urlsone[0])
#for uso in urlsone:
resoo = requests.get(urlsone[0])
resoo.encoding = 'utf-8'
bsoo = BeautifulSoup(resoo.text, 'html.parser')
lstoo = bsoo.select('a')
#    urlsoo = []
urlsoo=[]
for lsto in lstoo:
    if lsto.has_attr('href') and '/vod/' in lsto['href'] \
            and lsto['href'].endswith('.html'):
        urlsoo.append(sourceurl.rstrip('/')+lsto['href'])
print(urlsoo)
print(len(urlsoo))