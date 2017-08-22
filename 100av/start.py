#For get sed&pic
#fileauthor:Maser
#date:2016-12-20;20:14
import re
import requests
from bs4 import BeautifulSoup
def getTheUrl(srcUrl):
    resone=requests.get(srcUrl)
    resone.encoding='utf-8'
    bsone=BeautifulSoup(resone.text,'html.parser')
    #get all kinds of url
    lstotal=bsone.select('a')
    return lstotal

#the enter gate
#get all kinds of yellow url
sourceurl = 'https://8888av.co/'
lstone=getTheUrl(sourceurl)
urlsone=[]
for lst in lstone:
    if lst.has_attr('href') and '/list/' in lst['href']:
        if sourceurl.rstrip('/')+lst['href'] not in urlsone:
            urlsone.append(sourceurl.rstrip('/')+lst['href'])
print len(urlsone)
#iterator each kind
#for uso in urlsone:
print urlsone[0]
lstoo = getTheUrl(urlsone[0])
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
print len(urlsooo)
#get info & ed2k & pic
moviename=[]
torrent=[]
pic=[]
i = 0
head = {'user-agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}
for av in urlsooo:
    fp = open('%d.jpg'%i,'wb')
    resav=requests.get(av)
    resav.encoding='utf-8'
    avsop=BeautifulSoup(resav.text,'html.parser')
    #get the pic's url
    pic = 'https:' + avsop.find_all('div',class_="pic")[0].select('img')[0]['src']
    picUrl = str(pic)
    picp = requests.get(picUrl,headers=head)
    fp.write(picp.content)
    fp.close()
    print type(picUrl)
    #avtemlst=avsop.select('h1')
    #get the mnovie name
    avtemlst = avsop.find_all('div',class_='title')[-1].select('span')[0].text #bs4.element.Tag has such atrrs:find_all、select,both of them return a list,inside the list still Tag
    for avtem in avtemlst:
        print avtem.text
        moviename.append(avtem.text)
    avtemtt=avsop.select('textarea')
 #   aa=re.match(r"ed2k.*|/",avtemtt[0])
    for avtemt in avtemtt:
        torrent.append(avtemt.text)
    i +=1
    break
print torrent
#print(dict(zip(moviename,torrent)))