# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.spiders import Spider
from MyScrapy.items import FGWItem, parasItem
import scrapy
from Method import method
import urllib.request

class FGWSpider(Spider):
    name = 'FGW'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    VIEWSTATE=''
    EVENTVALIDATION=''
    childrenList=[]

    def start_requests(self):
        url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
        paras= method.get_hiddenvalue('http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx')
        self.VIEWSTATE=paras[0]
        self.EVENTVALIDATION=paras[1]
        paras_item = parasItem()
        paras_item['VIEWSTATE'] = self.VIEWSTATE
        paras_item['EVENTVALIDATION'] =self.EVENTVALIDATION

        yield scrapy.FormRequest(
            url=url,
            formdata={"__EVENTARGUMENT":"1",
                      "__EVENTTARGET":"AspNetPager1",
                      "ddlBwdw": 'nyj',#单位
                      "timeEndText": "2018-3-26",
                      "__EVENTVALIDATION":self.EVENTVALIDATION,
                      "__VIEWSTATE":self.VIEWSTATE,
                      "OrderFieldTextBox":"SerialNumber",
                      "OrderModeTextBox":"desc",
                    "AspNetPager1_input":"3"},
            callback=self.parse_page
        )



    def parse_page(self, response):
        ifEnd = response.xpath('//a[@disabled]/text()').extract()
        pageNow = response.xpath(r'//span/b/font[@color="red"]/text()').extract()
        pageNext=int(pageNow[0])+1
        urls2do = response.xpath('//table[@class="xxgk_table2"]/tr/td[@onmouseover="kfmo(event,this)"]/a/@href').extract()
        base_url = 'http://zfxxgk.ndrc.gov.cn/'
        for url2do in urls2do:
            new_url = base_url+url2do
            self.childrenList.append(new_url)
        if ifEnd:
            if ifEnd[0]==r'下一页':
                print("结束")
                yield Request(self.childrenList[0], callback=self.parse, dont_filter=True)
            else:
                url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
                VIEWSTATE = self.VIEWSTATE
                EVENTVALIDATION = self.EVENTVALIDATION

                yield scrapy.FormRequest(
                    url=url,
                    formdata={"__EVENTARGUMENT": str(pageNext),
                              "__EVENTTARGET": "AspNetPager1",
                              "ddlBwdw": 'nyj',  # 单位
                              "timeEndText": "2018-3-26",
                              "__EVENTVALIDATION": EVENTVALIDATION,
                              "__VIEWSTATE": VIEWSTATE,
                              "OrderFieldTextBox": "SerialNumber",
                              "OrderModeTextBox": "desc",
                              "AspNetPager1_input": "3"},
                    callback=self.parse_page
                )
        else:
            url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
            VIEWSTATE = self.VIEWSTATE
            EVENTVALIDATION = self.EVENTVALIDATION

            yield scrapy.FormRequest(
                url=url,
                formdata={"__EVENTARGUMENT":str(pageNext) ,
                          "__EVENTTARGET": "AspNetPager1",
                          "ddlBwdw": 'nyj',  # 单位
                          "timeEndText": "2018-3-26",
                          "__EVENTVALIDATION": EVENTVALIDATION,
                          "__VIEWSTATE": VIEWSTATE,
                          "OrderFieldTextBox": "SerialNumber",
                          "OrderModeTextBox": "desc",
                          "AspNetPager1_input": "3"},
                callback=self.parse_page
            )

    def parse(self, response):
        info_urls = self.childrenList
        not_urls=['http://zfxxgk.ndrc.gov.cn/PublicItemView.aspx?ItemID={e4fa98f2-01f0-4248-8da0-d498aa86643f}','http://zfxxgk.ndrc.gov.cn/PublicItemView.aspx?ItemID={73b2e7d9-f406-42a7-bf80-385f008afc75}']
        # for childurl in self.childrenList:
        for i in range(0, len(info_urls)):
            newinfourl = info_urls[i]
            if newinfourl not in not_urls:
                # self.getinfo(newinfourl)
                yield Request(newinfourl, callback=self.parse3)

    def parse3(self, response):
        item = FGWItem()
        title= response.xpath('//*[@id="out-content"]/div[2]/div/table/tr[1]/td/text()').extract()
        item['title'] = title
        content= response.xpath('//*[@id="ContentPanel"]')
        content = content.xpath('string(.)').extract()
        if content:
            content=content[0].strip()
        else:
            content=r'没有正文'
        item['content']=content
        date = response.xpath('//*[@id="out-content"]/div[2]/div/table/tr[3]/td[1]/text()').extract()
        if date:
            date = date[0].strip()
        else:
            date=r'1970-00-00'
        item['date'] = date
        item['url']=response.url
        yield item


