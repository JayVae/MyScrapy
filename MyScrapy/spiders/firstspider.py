# -*- coding: utf-8 -*-
import scrapy


class FirstspiderSpider(scrapy.Spider):
    name = "firstspider"
    allowed_domains = ["woodenrobot"]     #只爬该域名下的
    start_urls = ['http://woodenrobot.me']

    def parse(self, response):
        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print(title.strip())
        pass
