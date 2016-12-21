#For get sed&pic
#fileauthor:Maser
#date:2016-12-20;20:14
import re
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
#iterator each kind
#for uso in urlsone:
resoo = requests.get(urlsone[0])
resoo.encoding = 'utf-8'
bsoo = BeautifulSoup(resoo.text, 'html.parser')
lstoo = bsoo.select('a')
#    urlsoo = []
urlsoo=[]
#get the all links under current kind
for lsto in lstoo:
    if lsto.has_attr('href') and '/vod/' in lsto['href'] \
            and lsto['href'].endswith('.html'):
        urlsoo.append(sourceurl.rstrip('/')+lsto['href'])
#print(urlsoo)
del urlsoo[0]
urlsooo=[]
[urlsooo.append(x) for x in urlsoo if x not in urlsooo]
print(urlsooo)
#get info & ed2k & pic
moviename=[]
torrent=[]
pic=[]
for av in urlsooo:
    resav=requests.get(av)
    resav.encoding='utf-8'
    avsop=BeautifulSoup(resav.text,'html.parser')
    avtemlst=avsop.select('h1')
    for avtem in avtemlst:
        moviename.append(avtem.text)
    avtemtt=avsop.select('textarea')
 #   aa=re.match(r"ed2k.*|/",avtemtt[0])
    for avtemt in avtemtt:
        torrent.append(avtemt.text)
print(dict(zip(moviename,torrent)))