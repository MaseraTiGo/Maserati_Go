import scrapy
from dmys.items import DmysItem

class DmysSpider(scrapy.spiders.Spider):
    name = 'dmys'
    allowed_domains = ["cvcit.cn"]
    start_urls = ["http://cvcit.cn/"]
    
    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        for sel in response.xpath("//a[@class='videopic lazy xtcms']"):
            item = DmysItem()
            item['name'] = sel.xpath("@title").extract()[0]
            item['link'] = sel.xpath("@href").extract()[0]
            item['kind'] = 'film'
            yield item