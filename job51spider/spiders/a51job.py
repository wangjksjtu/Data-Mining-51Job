# -*- coding: utf-8 -*-
import scrapy
from ..items import Job51SpiderItem

class A51jobSpider(scrapy.Spider):
    name = '51job'

    # start_urls = ['https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C080200,000000,0000,01%252C37%252C32%252C38%252C40,9,99,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    def start_requests(self):
        urls = []
        for i in range(2000):
            urls.append(
                'https://search.51job.com/list/010000%252C020000%252C030200%252C040000%252C080200,000000,0100%252C2400%252C2500%252C2600%252C2700,00,9,99,%2B,2,'+str(i+1)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
            )
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        divs = response.xpath('//div[@id="resultList"]/div[@class="el"]/p/span/a/@href').extract()
        for div in divs:
            yield scrapy.Request(url=div, callback=self.getDetails)

    def getDetails(self, response):
        try:
            item = Job51SpiderItem()
            item['job']=response.xpath('//div[@class="tHeader tHjob"]//h1/text()')[0].extract()
            item['area']=response.xpath('//div[@class="tHeader tHjob"]//span[@class="lname"]/text()')[0].extract()
            item['company']=response.xpath('//p[@class="cname"]/a/text()')[0].extract()

            tmp = response.xpath('//p[@class="msg ltype"]/text()').extract_first().split('|')
            item['company_type']=tmp[0].strip()
            item['company_people']=tmp[1].strip()
            item['company_service']=tmp[2].strip()
            item['salary']=response.xpath('//div[@class="tHeader tHjob"]//div[@class="cn"]/strong/text()')[0].extract()
            item['welfare']=response.xpath('//p[@class="t2"]/span/text()').extract()
            item['work_experience']=response.xpath('//div[@class="t1"]//em[@class="i1"]/../text()').extract_first("无")
            item['education']=response.xpath('//div[@class="t1"]//em[@class="i2"]/../text()').extract_first("无")
            item['hire_num']=response.xpath('//div[@class="t1"]//em[@class="i3"]/../text()').extract_first("无")
            item['put_time']=response.xpath('//div[@class="t1"]//em[@class="i4"]/../text()').extract_first("无")
            item['language']=response.xpath('//div[@class="t1"]//em[@class="i5"]/../text()').extract_first("无")
            item['demand_profession']=response.xpath('//div[@class="t1"]//em[@class="i6"]/../text()').extract_first("无")

            item['job_info'] = ''.join(response.xpath(
                '//div[@class="bmsg job_msg inbox"]/p/text() | //div[@class="bmsg job_msg inbox"]/div/text()').extract())
            item['job_info'] = item['job_info'].strip()
            item['job_work_type'] = response.xpath(
                '//div[@class="bmsg job_msg inbox"]/div[@class="mt10"]//span[contains(text(),"职能类别")]/../span[@class="el"]/text()').extract()
            item['job_keyword'] = response.xpath(
                '//div[@class="bmsg job_msg inbox"]/div[@class="mt10"]//span[contains(text(),"关键字")]/../span[@class="el"]/text()').extract()
            yield item

        except:
            pass

