# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from scrapy.item import Item


class City58Pipeline(object):

    DB_URI = 'mongodb://localhost:27017'  # 数据库的uri地址
    DB_NAME = 'scrapy_data'  # 数据库名字

    def open_spider(self, spider):
        self.client = MongoClient(self.DB_URI)  # 数据库实例化
        self.db = self.client[self.DB_NAME]
        print('我开启了数据库连接了')

    def process_item(self, item, spider):
        collection = self.db[spider.name]  # 建表
        post = dict(item) if isinstance(item, Item) else item
        collection.insert_one(post)
        return item

    def close_spider(self, spider):
        self.client.close()
        print('我关闭数据库了')
