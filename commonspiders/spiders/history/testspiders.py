'''
from scrapy.spiders import CrawlSpider


class Spiders(CrawlSpider):
    name='commonspiders'
    allowed_domains=['http://www.goubanjia.com']
    start_urls=[]
    for i in range(1,11):
        url='http://www.goubanjia.com/index%d.shtml' %i
        start_urls.append(url)


    def parse(self, response):
        for res in response.xpath('//*[@id="list"]/table/tbody/tr'):
            iplist=[]
            for ress in res.xpath('td[@class="ip"]/*[not(@style="display: none;" or @style="display:none;")]/text()').extract():
              iplist.append(ress)
            iplist.insert(-1,':')
            ip=''.join(iplist)
            print(ip)
'''