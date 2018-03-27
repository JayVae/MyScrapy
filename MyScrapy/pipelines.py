# -*- coding: utf-8 -*-
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import json
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyscrapyPipeline(object):
    # 插入的sql语句
    feed_key = ['title', 'content', 'date', 'url', 'title2']
    insertFeed_sql = '''insert into MeiziFeed (%s) values (%s)'''
    feed_query_sql = "select * from MeiziFeed where feedId = %s"
    feed_seen_sql = "select feedId from MeiziFeed"
    max_dropcount = 50
    current_dropcount = 0

    def __init__(self):
        dbargs = settings.get('DB_CONNECT')
        db_server = settings.get('DB_SERVER')
        dbpool = adbapi.ConnectionPool(db_server, **dbargs)
        self.dbpool = dbpool
        # 更新看过的id列表
        d = self.dbpool.runInteraction(self.update_feed_seen_ids)
        d.addErrback(self._database_error)

    def __del__(self):
        self.dbpool.close()

    # 更新feed已录入的id列表
    def update_feed_seen_ids(self, tx):
        tx.execute(self.feed_seen_sql)
        result = tx.fetchall()
        if result:
            # id[0]是因为result的子项是tuple类型
            self.feed_ids_seen = set([int(id[0]) for id in result])
        else:
            # 设置已查看过的id列表
            self.feed_ids_seen = set()

    # 处理每个item并返回
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self._database_error, item)

        feedId = item['url']
        if (int(feedId) in self.feed_ids_seen):
            self.current_dropcount += 1
            if (self.current_dropcount >= self.max_dropcount):
                spider.close_down = True
            raise DropItem("重复的数据:%s" % item['feedId'])
        else:
            return item

    # 插入数据
    def _conditional_insert(self, tx, item):
        # 插入Feed
        tx.execute(self.feed_query_sql, (item['feedId']))
        result = tx.fetchone()
        if result == None:
            self.insert_data(item, self.insertFeed_sql, self.feed_key)
        else:
            print
            "该feed已存在数据库中:%s" % item['feedId']
        # 添加进seen列表中
        feedId = item['feedId']
        if int(feedId) not in self.feed_ids_seen:
            self.feed_ids_seen.add(int(feedId))
        # 插入User
        user = item['userInfo']
        tx.execute(self.user_query_sql, (user['userId']))
        user_result = tx.fetchone()
        if user_result == None:
            self.insert_data(user, self.insertUser_sql, self.user_key)
        else:
            print
            "该用户已存在数据库:%s" % user['userId']
        # 添加进seen列表中
        userId = user['userId']
        if int(userId) not in self.user_ids_seen:
            self.user_ids_seen.add(int(userId))

    # 插入数据到数据库中
    def insert_data(self, item, insert, sql_key):
        fields = u','.join(sql_key)
        qm = u','.join([u'%s'] * len(sql_key))
        sql = insert % (fields, qm)
        data = [item[k] for k in sql_key]
        return self.dbpool.runOperation(sql, data)

    # 数据库错误
    def _database_error(self, e):
        print
        "Database error: ", e
