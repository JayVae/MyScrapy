# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 排名
    # ranking = scrapy.Field()
    # # 电影名称
    # movie_name = scrapy.Field()
    # # 评分
    # score = scrapy.Field()
    # # 评论人数
    # score_num = scrapy.Field()


    project_id = scrapy.Field()
    project_name = scrapy.Field()
    project_company = scrapy.Field()
    project_type = scrapy.Field()
    # 审批部门
    approve_department = scrapy.Field()
    approve_item = scrapy.Field()
    approve_result = scrapy.Field()
    approve_date = scrapy.Field()
    approve_number = scrapy.Field()

    pass

class FGWItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    url=scrapy.Field()
    # title2 = scrapy.Field()
    pass

class parasItem(scrapy.Item):
    VIEWSTATE=scrapy.Field()
    EVENTVALIDATION=scrapy.Field()


class SplashTestItem(scrapy.Item):
    #单价
    price = scrapy.Field()
    # description = Field()
    #促销
    promotion = scrapy.Field()
    #增值业务
    value_add = scrapy.Field()
    #重量
    quality = scrapy.Field()
    #选择颜色
    color = scrapy.Field()
    #选择版本
    version = scrapy.Field()
    #购买方式
    buy_style=scrapy.Field()
    #套装
    suit =scrapy.Field()
    #增值保障
    value_add_protection = scrapy.Field()
    #白天分期
    staging = scrapy.Field()
    # post_view_count = scrapy.Field()
    # post_comment_count = scrapy.Field()
    # url = scrapy.Field()