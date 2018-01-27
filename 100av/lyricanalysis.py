# -*- coding: utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import time

re_words = re.compile(u"[\u4e00-\u9fa5]+")
sourceurl =['http://www.kuwo.cn/playlist/index?pid=297190019','http://www.kuwo.cn/playlist/index?pid=2380305372']
c = 0
a = 0
songUrlList = []
ff = open('d:\\dongye.txt','w')
def getTheUrl(srcUrl):
    resone=requests.get(srcUrl)
    #resone.encoding='utf-8'
    bsone=BeautifulSoup(resone.text,'html.parser')
    lstotal=bsone.select('a')
    return lstotal
    
for url in sourceurl:
    lst = getTheUrl(url)
    for lstt in lst:
        if lstt.has_attr('href') and re.search('yueku\d+',lstt['href']):
            songUrlList.append(lstt['href'])
        #if songUrlList.__len__() > 10:break
totalSong = len(songUrlList)
print totalSong,'--------------------------------'
for item in songUrlList:
    print item 
    try:
        res = requests.get(item)    
    #fuck1 = requests.get('http://www.kuwo.cn/yinyue/900497?catalog=yueku2016')
        resn=BeautifulSoup(res.text,'html.parser')
    #print bbb.text
        lyricSrc = resn.select('script')[6].text
        m = re_words.findall(lyricSrc,0)
        for item in m:
            ff.write(item.encode('utf-8') + '\n')
        ff.write('======\n')
        totalSong -= 1
        c += 1
        if c%10 == 0:time.sleep(2)
    except Exception,e:
        print e
        continue
    print '%d song left now!!!'%totalSong