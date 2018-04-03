from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from selenium import webdriver
import re
import json
import time
import commonspiders.tool as tool
import os

file_name='双桥'
img_dir='D:/photo/20171020/'
imgdir3='D:/photo/美团logo/'



def get_data(url):
    mobileEmulation = {'deviceName': 'iPhone 6 Plus'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('mobileEmulation', mobileEmulation)
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe',
                              chrome_options=options)
    driver.set_page_load_timeout(100)
    driver.set_script_timeout(100)
    driver.get(url)
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="menu-tabs-container"]/div/a[3]/span').click()
    time.sleep(3)
    name = driver.find_element_by_xpath('//*[@id="header"]/h1/span').text
    phone = driver.find_element_by_xpath('//*[@id="detail-wrap"]/div[1]/div/div[1]/p').text
    shopaddress=driver.find_element_by_xpath('//*[@id="detail-wrap"]/div[1]/div/div[2]/p').text
    deliverytime=driver.find_element_by_xpath('//*[@id="detail-wrap"]/div[2]/div/div[1]/p').text
    deliveryservice=driver.find_element_by_xpath('//*[@id="detail-wrap"]/div[2]/div/div[2]/p').text
    data='%s[}%s[}%s[}%s[}%s[}%s' %(url,name,phone,shopaddress,deliverytime,deliveryservice)
    driver.quit()
    return data

def get_url(url):
    print(url)
    driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver2.30.exe')
    driver.set_page_load_timeout(100)
    driver.set_script_timeout(100)
    driver.get(url)
    fllow_url=driver.find_element_by_xpath('//a[@class="provider_name"]').get_attribute('href')
    return fllow_url


class Spiders(CrawlSpider):
    name='commonspiders'
    #allowed_domains = ["dianping.com"]
    #start_urls=['http://www.dianping.com/shop/10388291']
    #for i in range(1,11):
    #    url='http://www.goubanjia.com/index%d.shtml' %i
    #    start_urls.append(url)
    #with open('C:/Users/Administrator/Desktop/commons/2017-3-23/commons_foodhost_detail_0.txt', 'r',encoding='utf-8') as f:
     #   for line in f:
     #       temp.append(line.split('[}')[-1].replace('\n', ''))

    #with open('C:/Users/Administrator/Desktop/20171019_0.txt', 'r', encoding='utf-8') as f:
    #    for line in f:
     #       url = 'http://cd.meituan.com/s/' + str(line.split('[}')[0])
     #       start_urls.append(url)

    #with open('C:/Users/Administrator/Desktop/旅游/list.txt', 'r', encoding='utf-8') as f:
    #    for line in f:
    #        url = 'http://%s' % line.replace('\n', '')
    #        start_urls.append(url)
    '''
    regsionlist=[]
    success=[]
    dailist=[]
    with open('C:/Users/Administrator/Desktop/regsion.txt', 'r', encoding='utf-8') as f:
        for line in f:
            regsionlist.append(line.replace('\n',''))
    with open('C:/Users/Administrator/Desktop/success1107.txt', 'r', encoding='utf-8') as f:
        for line in f:
            success.append(line.replace('\n','').split('[}')[2])
    for i in regsionlist:
        #print(i.split('[}')[2])
        if i.split('[}')[2] not in success:
            dailist.append(i)
    print(dailist)
    '''



    def start_requests(self):
        '''
        #url='http://www.dianping.com/shop/10388291'
        yield Request(url=url, cookies={'_lxsdk':'15f3553034dc8-0141dfabc65749-333f5902-1fa400-15f3553034dad',
                                         '_lxsdk_cuid':'15f3553034dc8-0141dfabc65749-333f5902-1fa400-15f3553034dad ',
                                         '_hc.v':'a7e3dbcb-3761-ce4e-97bc-25435354f265.1508428154',
                                         'Hm_lvt_dbeeb675516927da776beeb1d9802bd4':'1509338424',
                                         'Hm_lpvt_dbeeb675516927da776beeb1d9802bd4':'1509338424',
                                         '__mta':'142520845.1508469107229.1509338420579.1509338423923.33',
                                         'JSESSIONID':'E29C9846C95CEA0722AC2D575AFC4B70',
                                         '__utma':'1.1653769848.1508989979.1509937846.1509939999.10',
                                         '__utmc':'1',
                                         'cye':'8',
                                         '_lxsdk_s':'15f8fa3f14c-014-ba9-967%7C%7C71',
                                         '_hc.v':'a7e3dbcb-3761-ce4e-97bc-25435354f265.1508428154'
                                        }, callback=self.parse)
        '''
        for i in self.dailist:
             url='http://api.mobile.meituan.com/group/v4/poi/pcsearch/59?' \
                 'uuid=7fc7dd7ace2f44ae6b68.1508473122.5.0.1&userid=203793564&limit=1&offset=0&areaId=%s&cateId=1' \
                  %i.replace('\n','').split('[}')[-2].split('b')[-1]
             yield Request(url=url,meta={'district':i.split('[}')[0],'street':i.split('[}')[2],'i':i},callback=self.parse)

    def parse(self, response):
        totalCount = str(re.findall('\"totalCount\":(.*?),', str(response.body))[0])
        i=response.meta['i']
        url = 'http://api.mobile.meituan.com/group/v4/poi/pcsearch/59?' \
              'uuid=7fc7dd7ace2f44ae6b68.1508473122.5.0.1&userid=203793564&limit=%s&offset=0&areaId=%s&cateId=1' \
              %( totalCount,i.replace('\n', '').split('[}')[-2].split('b')[-1])
        yield Request(url=url, meta={'district': i.split('[}')[0], 'street': i.split('[}')[2], 'i': i},
                      callback=self.parse1)

    def parse1(self, response):
        #if int(totalCount)>=1000:
        #    print('数量大于1000'+response.url)
        #    return None
        print(response.url)
        regx='\"searchResult\":(.*?),\"cardExtension\"'
        data=re.findall(regx,str(response.body.decode('utf-8')))[0]
        for jsondata in json.loads(data):
            id=jsondata['id']
            title=jsondata['title']
            address=jsondata['address']
            logo=jsondata['imageUrl'].replace('w.h/','').replace('*','')
            logname=title+'_logo.jpg'
            try:
              tool.GetImg(imgdir3, logo, logname)
            except:
              logname=''

            avgprice=jsondata['avgprice']
            lowestprice=jsondata['lowestprice']
            lat=jsondata['latitude']
            lng=jsondata['longitude']
            avgscore=jsondata['avgscore']
            comments=jsondata['comments']
            backCateName=jsondata['backCateName']
            if backCateName=='鲜花店' or backCateName=='茶馆'or backCateName=='酒店':
                continue
            district=response.meta['district']
            street=response.meta['street']
            d='%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s[}%s' %(id,title,address,avgprice,logo,logname,lowestprice,lat,lng,avgscore,comments,backCateName,district,street)
            with open('C:/Users/Administrator/Desktop/meituanbasic20171113.txt', 'a', encoding='utf-8') as f:
                f.write(d)
                f.write('\n')
        with open('C:/Users/Administrator/Desktop/success1107.txt', 'a', encoding='utf-8') as f:
            f.write(response.meta['i'])
            f.write('\n')

        '''
        shop_id = response.url.split('/')[-3]  # 店铺ID

        for sel in response.xpath('//div[@class="picture-list"]/ul/li'):
            img=sel.xpath('div/a/img/@src').extract_first()
            img_name =img.split('/')[-1]
            data='%s[}%s' %(shop_id,img)
            with open('C:/Users/Administrator/Desktop/shop_huanjing.txt', 'a', encoding='utf-8') as f:
                  f.write(data)
                  f.write('\n')
            tool.GetImg(img_dir,img,img_name)

        for res in response.xpath('//*[@id="list"]/table/tbody/tr'):
            iplist=[]
            for ress in res.xpath('td[@class="ip"]/*[not(@style="display: none;" or @style="display:none;")]/text()').extract():
              iplist.append(ress)
            iplist.insert(-1,':')
            ip=''.join(iplist)
            print(ip)
        '''

        #name=str(response.xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[1]/a/span/text()').extract_first())
        #address=response.xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[2]/div[2]/p[2]/text()').extract_first()
        #phone=str(response.xpath('//div[@class="telephone"]/p[@class="poi-detail-right"]/text()').extract_first())
        #print('%s[}%s[}%s[}%s' % (response.url, name, phone, address))
        #if phone!='None':
            #name,phone = get_phone(response.url)
        #get_url(response.url)

    '''
    def parse(self, response):
        name=''.join(response.xpath('//*[@id="main"]/div/h2/text()').extract()).replace('\n','').replace(' ','').replace('/','')
        type = response.xpath('//*[@id="main"]/div/h2/a[2]/text()').extract_first()
        host=response.xpath('//div[@class="nutr-tag margin10"]/div[1]/dl[2]/dd[1]/span[2]/span/text()').extract_first()
        carbohydrate=response.xpath('//div[@class="nutr-tag margin10"]/div[1]/dl[2]/dd[2]/span[2]/text()').extract_first()
        fat=response.xpath('//div[@class="nutr-tag margin10"]/div[1]/dl[3]/dd[1]/span[2]/text()').extract_first()
        proteide=response.xpath('//div[@class="nutr-tag margin10"]/div[1]/dl[3]/dd[2]/span[2]/text()').extract_first()
        data='%s[}%s[}%s[}%s[}%s[}%s[}%s' %(name,type,host,fat,carbohydrate,proteide,response.url.replace('http://www.boohee.com',''))
        if 'None' in data:
            yield Request(url=response.url,dont_filter=True, callback=self.parse)
        if 'None' not in data:
            print(data)
            tool.GetFile('foodhost_detail', data, 3, 10000)

    start_urls=['http://www.boohee.com/food/group/1?page=1','http://www.boohee.com/food/group/2?page=1','http://www.boohee.com/food/group/3?page=1',
                'http://www.boohee.com/food/group/4?page=1','http://www.boohee.com/food/group/5?page=1','http://www.boohee.com/food/group/6?page=1',
                'http://www.boohee.com/food/group/7?page=1','http://www.boohee.com/food/group/8?page=1','http://www.boohee.com/food/group/9?page=1',
                'http://www.boohee.com/food/group/10?page=1','http://www.boohee.com/food/view_menu?page=1',
               ]

    def parse(self, response):
        page=int(response.url.split('=')[-1])
        if(page>10):
            return None
        type=response.xpath('//*[@id="main"]/div/div[2]/h3/text()').extract_first().replace('\n','')
        for sel in response.xpath('//*[@id="main"]/div/div[2]/ul/li'):
            food_url=sel.xpath('div[@class="text-box pull-left"]/h4/a/@href').extract_first()
            name=','.join(sel.xpath('div[@class="text-box pull-left"]/h4/a/text()').extract()).replace('\n','')
            host=sel.xpath('div[@class="text-box pull-left"]/p/text()').extract_first().replace('\n','')
            data='%s[}%s[}%s[}%s' %(name,host,type,food_url)
            tool.GetFile('foodhost',data,3,10000)
        follow_url='%s=%s' %(response.url.split('=')[0] ,(page+1))
        yield Request(url=follow_url,callback=self.parse)
        '''
