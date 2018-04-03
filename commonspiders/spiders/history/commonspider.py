from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
import re
import json
import time
import commonspiders.tool as tool


class Spiders(CrawlSpider):
    name='temp_commonspiders'
    #allowed_domains=['']
    #start_urls=['http://coral.qq.com/article/1776948078/comment?commentid=0&reqnum=20&tag=&callback=mainComment&_=1488333872637']
    #start_urls=['http://comment.money.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CDSE5KHF002580S6/comments/newList?offset=0&limit=30&_=%s'%str(time.time()).split('.')[0]]
    company_mark=[]
    company_content=[]
    start_urls=['http://h5.dianping.com/platform/secure/index.html?returl=http://www.dianping.com/shop/22584878/review_all?pageno=2']
    #start_urls=['http://www.baidu.com/s?wd=%E6%99%AF%E5%92%8C%E5%8D%83%E5%9F%8E&pn=10&oq=%E6%99%AF%E5%92%8C%E5%8D%83%E5%9F%8E&ie=utf-8&usm=2&rsv_pq=85e3b08200018c3d']
    #start_urls=['http://www.zbj.com/dshy/s.html','http://www.zbj.com/dshy/sp2.html','http://www.zbj.com/dshy/sp3.html',
    #           'http://www.zbj.com/dshy/sp4.html','http://www.zbj.com/dshy/sp5.html','http://www.zbj.com/dshy/sp6.html',
    #           'http://www.zbj.com/cyhy/s.html','http://www.zbj.com/cyhy/sp2.html','http://www.zbj.com/sqwy/s.html',
    #            'http://www.zbj.com/jypx/s.html','http://www.zbj.com/jypx/sp2.html','http://www.zbj.com/wlps/s.html',
    #            'http://www.zbj.com/ylhy/s.html','http://www.zbj.com/lycx/s.html','http://www.zbj.com/qcfw/s.html',
    #            'http://www.zbj.com/hrrj/sq10031087.html','http://www.zbj.com/scmrj/sq10031102.html','http://www.zbj.com/cwrj/sq10031072.html',
    #            'http://www.zbj.com/xmrj/sq10031104.html','http://www.zbj.com/fxrj/sq10031111.html','http://www.zbj.com/wlw/sq10030949.html',
    #            'http://www.zbj.com/hlwyy/sq10030952.html','http://www.zbj.com/ccwl/sq10030972.html']
    #with open('C:/Users/Administrator/Desktop/commons/2017-3-23/commons_address_0.txt', 'r', encoding='utf-8') as f:
    #    for line in f:
    #       company_mark.append(line.replace('\n', ''))
    #        start_urls.append(line.split('[}')[1])#.strip().replace('\n', ''))
    def parse1(self, response):
        for sel in response.xpath('//div[@class="service-item picView-item"]'):
            titile=sel.xpath('div[@class="service-desc"]/a/text()').extract_first()
            follow_url=sel.xpath('div[@class="service-desc"]/a/@href').extract_first()
            #content=','.join(sel.xpath('div[2]/div/div/p[@class="like"]/a/text()').extract())
            company=sel.xpath('div[@class="btm-line clearfix"]/div/a/text()').extract_first()
            type=sel.xpath('div[2]/div/div/p[2]/text()').extract_first()
            data='%s[}%s[}%s' %(titile,follow_url,company)
            tool.GetFile('address',data,3,100000)
            #yield Request(url=follow_url,meta={"content":data},callback=self.parse1)

    def parse(self,response):
        img=response.xpath('//div[@class="container"]').extract()
        print(img)
        #content=response.meta["content"]
        #phone=','.join(response.xpath('//div[@class="time-item"]/text()').extract()).replace('\n','').replace(' ','')
        #for i in self.company_mark:
        #    if response.url in i:
        #        data = '%s[}%s' % (i,phone)
        #        tool.GetFile('2017324', data, 3, 100000)
    '''
    def parse(self, response):
        page=int(str(response.url).split('&')[1].split('=')[1])+10
        mark=response.xpath('//*[@id="rs"]/table/*/*/a/text()').extract()
        for i in mark:
         if i not in self.company_mark:
             self.company_mark.append(i)
             tool.GetFile('company_mark', i, 3, 10000)
        for sel in  response.xpath('//*[@id="content_left"]/*/h3'):
            content = ''.join(sel.xpath('a//text()').extract())
            data='%s[}%s' %(content,time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            if data not in self.company_content:
               self.company_content.append(data)
               tool.GetFile('company',data,3,10000)
        follow_url='http://www.baidu.com/s?wd=%E6%99%AF%E5%92%8C%E5%8D%83%E5%9F%8E&pn='+str(page)+'&oq=%E6%99%AF%E5%92%8C%E5%8D%83%E5%9F%8E'
        if page==1000:
            return None
        yield Request(url=follow_url,callback=self.parse)
    '''
    '''
    def parse(self, response):
        data=response.body_as_unicode()
        mydata = re.findall('\"comments\":(.*?),\"newListSize\"', data)[0]
        page=int(re.findall('offset=(.*?)&', response.url)[0])+30
        data = re.findall('({"commentId".*?"})[,"|}?,?]', mydata)
        for i in data:
            print(i)
        for i in json.loads(mydata):
            data=re.findall('\"'+i+'\":({"commentId".*"})}?,?', mydata)[0]
            json_data=json.loads(data)
            commentId=i
            content=json_data['content']
            createtime=json_data['createTime']
            sitename = json_data['siteName']
            user_id=json_data['user']['userId']
            nickname=json_data['user']['nickname']
            location=json_data['user']['location']
            file_data='%s[}%s[}%s[}%s[}%s[}%s[}%s' %(commentId,content,createtime,sitename,user_id,nickname,location)
            tool.GetFile('common_wangyi',file_data,3,10000)
        if len(json.loads(mydata))<30:
           return None
        follow_url='http://comment.money.163.com/api/v1/products/a2869674571f77b5a0867c3d71db5856/threads/CDSE5KHF002580S6/comments/newList?offset=%d&limit=30&_=%s'%(page,str(time.time()).split('.')[0])
        yield Request(url=follow_url,callback=self.parse)
    '''
    '''
    def parse(self, response):
        data=response.body_as_unicode()
        mydata=re.findall('\"data\":(.*?),\"targetinfo\"',data)[0]
        last_id = re.findall('\"last\":\"(.*?)\"',data)[0]
        retnum  = re.findall('\"retnum\":(.*?),',data)[0]
        myjson=re.findall('\"commentid\":(.*?),\"targetinfo\"',data)[0]
        for i in json.loads(myjson):
            id=i['id']
            parent=i['parent']
            content=''.join(re.findall(u"[\u4e00-\u9fa5_a-zA-Z0-9]|[\（\）\《\》\——\；\，\。\‘\’\“\”\<\>\！\《\》\【\】\*\&\……\￥\#\@\~]|[\^,.!`?+=\_\-:;\']",i['content']))
            timeDifference=i['timeDifference']
            up=i['up']
            rep=i['rep']
            file_data='%s{]%s{]%s{]%s{]%s{]%s' %(id,parent,content,timeDifference,up,rep)
            tool.GetFile('dacheng',file_data,3,5000)
        fllow_url='http://coral.qq.com/article/1776948078/comment?commentid=%s&reqnum=20&tag=&callback=mainComment&_=%s' %(last_id,str(time.time()).split('.')[0])
        if int(retnum)<20:
            return None
        yield Request(url=fllow_url,callback=self.parse)
    '''
