#encoding:utf-8
import requests
import time
import re
import json
from bs4 import BeautifulSoup as bs
def getRes(url):
    return requests.get(url).content
srct = format('%0.3f'%time.time())
tt = lambda x: reduce(str.__add__,x.split('.'))
t = int(tt(srct))
tb = str(t-100)
t = str(t)
url = 'https://www.vmall.com/product/738677717.html'
reurl = 'https://remark.vmall.com/remark/queryPrdinfoEvaluateScore.json?pid=738677717&t=%s&callback=jsonp%s'%(t,tb)
res = requests.get(url)
res2 = requests.get(reurl)
totalPrdCount = res2.text.split(':')[-1][:5]
html = bs(res.text,'html.parser')
#html = html.select('a')
print html.find_all('a',id='pro-tab-evaluate')[0].text + ':' + totalPrdCount

for i in xrange(10):
    urlCom = 'https://remark.vmall.com/remark/queryEvaluate.json?pid=738677717&pageNumber=%d&t=%s&callback=jsonp%s'%(i+1,t,tb)
    print getRes(urlCom)[19:-2]
    break
    