# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from MyScrapy.items import FGWItem
import scrapy
from Method import method

class FGWSpider(Spider):
    name = 'FGW'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
        paras= method.get_hiddenvalue('http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx')
        VIEWSTATE=paras[0]
        EVENTVALIDATION=paras[1]

        yield scrapy.FormRequest(
            url=url,
            formdata={"__EVENTARGUMENT":"4",
                      "__EVENTTARGET":"AspNetPager1",
                      "ddlBwdw": 'nyj',#单位
                      "timeEndText": "2018-3-26",
                      "__EVENTVALIDATION":EVENTVALIDATION,
                      "__VIEWSTATE":VIEWSTATE,
                      "OrderFieldTextBox":"SerialNumber",
                      "OrderModeTextBox":"desc",
                    "AspNetPager1_input":"3"},
            callback=self.parse_page
        )


    def parse_page(self, response):
        # //*[@id="DataGridView_ctl04_HyperLink1"]
        # //*[@id="DataGridView_ctl02_HyperLink1"]
        ifEnd = response.xpath('//a[@disabled]/text()').extract()
        # /html/body/form/div[2]/div[5]/div[1]/span[1]
        # <span style="margin-right:5px;font-weight:Bold;color:red;">2</span>
        # <span><b><font color="red">1</font></b>
        pageNow = response.xpath(r'//span/b/font[@color="red"]/text()').extract()
        pageNext=int(pageNow[0])+1
        print(pageNext)
        urls2do = response.xpath('//table[@class="xxgk_table2"]/tr/td[@onmouseover="kfmo(event,this)"]/a/@href').extract()
        base_url = 'http://zfxxgk.ndrc.gov.cn/'
        for url2do in urls2do:
            new_url = base_url+url2do
            print(new_url)
            yield Request(new_url,headers=self.headers,callback=self.parse)
        if ifEnd:
            if ifEnd[0]==r'下一页':
                print("结束")
            else:
                print("不是结束")
                url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
                paras = method.get_hiddenvalue('http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx')
                VIEWSTATE = paras[0]
                EVENTVALIDATION = paras[1]

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
            print("不是结束")
            url = 'http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx'
            paras = method.get_hiddenvalue('http://zfxxgk.ndrc.gov.cn/PublicItemList.aspx')
            VIEWSTATE = paras[0]
            EVENTVALIDATION = paras[1]

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



    def parse2(self,response):
        pass


    def parse(self,response):
        # //*[@id="ContentPanel"]/p[1]/span/strong/span
        item = FGWItem()
        title= response.xpath('//*[@id="ContentPanel"]/p[1]/span/strong/span/text()').extract()
        item['title'] = title
        print(11111)
        item['content'] = response.xpath('//*[@id="ContentPanel"]/p[3]/span/span/text()').extract()
        item['date'] = response.xpath('//*[@id="out-content"]/div[3]/div/table/tr[3]/td[1]/text()').extract()
        yield item




        # ifEnd = response.xpath('//a/@disabled').extract()

