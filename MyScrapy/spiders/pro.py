# -*- coding: utf-8 -*-
import re

from scrapy.spiders import Spider
from MyScrapy.items import MyscrapyItem
from scrapy import Request

class TransformerSpider(Spider):
    name = 'trans'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://www.xjtzxm.gov.cn/toXmbljggs.jspx?pageNo=1'
        yield Request(url, headers=self.headers, callback=self.parse3)

    def parse3(self, response):
        pageMax = response.xpath('//input[@id="zys"]/@value').extract()[0]
        base = 'http://www.xjtzxm.gov.cn/toXmbljggs.jspx?pageNo='
        page_no_now = 1
        while(page_no_now <= int(pageMax)):
            url = base + str(page_no_now)
            page_no_now = page_no_now +1
            yield Request(url, headers=self.headers, callback=self.parse)

    def parse2(self, response):
        item = MyscrapyItem()
        item['project_id'] = response.xpath('/html/body/div[2]/table[1]/tbody/tr[1]/td[2]/text()').extract()[0].strip()
        item['project_name']= response.xpath('/html/body/div[2]/table[1]/tbody/tr[1]/td[4]/@title').extract()[0].strip()
        item['project_company']= response.xpath('/html/body/div[2]/table[1]/tbody/tr[2]/td[4]/text()').extract()[0].strip()
        item['project_type']= response.xpath('/html/body/div[2]/table[1]/tbody/tr[2]/td[2]/text()').extract()[0].strip()
        item['approve_department']= response.xpath('/html/body/div[2]/table[2]/tbody/tr/td[1]/text()').extract()[0].strip()
        item['approve_item']= response.xpath('/html/body/div[2]/table[2]/tbody/tr/td[2]/@title').extract()[0].strip()
        item['approve_result']= response.xpath('/html/body/div[2]/table[2]/tbody/tr/td[3]/text()').extract()[0].strip()
        item['approve_date']= response.xpath('/html/body/div[2]/table[2]/tbody/tr/td[4]/text()').extract()[0].strip()
        item['approve_number']= response.xpath('/html/body/div[2]/table[2]/tbody/tr/td[5]/text()').extract()
        yield item

    def parse(self, response):
        # pageMax = response.xpath('//input[@id="zys"]/@value')
        projects = response.xpath('/html/body/div[2]/table/tbody//@onclick').extract()
        base_url = 'http://www.xjtzxm.gov.cn/toTkxmblsx.jspx?'
        for pro in projects:
            pro=pro.split('\'')
            info_url=base_url+'projectId='+pro[1]+'&sxbh='+pro[3]+'&sxzxbh='+pro[5]+'&userId='+pro[7]+'&cbsnum='+pro[9]
            yield Request(info_url, callback=self.parse2)


