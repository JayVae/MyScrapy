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
    pass
