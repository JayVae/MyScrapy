# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class Spider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = []
    start_urls = ['https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                                args={'wait': 0.5}, endpoint='render.html',headers=self.headers)

    def parse(self, response):
        # //*[@id="J_Itemlist_TLink_560681958734"]
        titele = response.xpath('//div[@class="row row-2 title"]/a/text()').extract()
        print('这是标题：', titele)