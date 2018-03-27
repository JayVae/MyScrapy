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
        # for childurl in self.childrenList:
        for i in range(0, len(info_urls)):
            newinfourl = info_urls[i]
            # self.getinfo(newinfourl)
            yield Request(newinfourl, callback=self.parse3)

    def parse3(self, response):
        item = FGWItem()
        # /html/body/form/div[2]/div/div[3]/div/div[2]
        # //*[@id="out-content"]/div[2]/div/div[2]
        # //*[@id="ContentPanel"]/p[1]/span/strong/span
        title= response.xpath('//*[@id="out-content"]/div[2]/div/div[2]/text()').extract()
        title2=response.xpath('//*[@id="ContentPanel"]/p[1]/span/strong/span/text()').extract
        item['title'] = title
        item['title2']=title2
        # /html/body/form/div[2]/div/div[3]/div/div[4]/div[1]/p/span
        # //*[@id="ContentPanel"]/p[1]/span
        item['content'] = response.xpath('//*[@id="ContentPanel"]/p/span/span/text()').extract()
        # /html/body/form/div[2]/div/div[3]/div/table/tbody/tr[3]/td[1]
        item['date'] = response.xpath('//*[@id="out-content"]/div[2]/div/table/tr[3]/td[1]/text()').extract()
        item['url']=response.url
        print(item)
        yield item


