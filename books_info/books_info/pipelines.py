# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymongo
from scrapy.item import Item
from scrapy.exceptions import DropItem
"""
在管道中要么return item 要么抛弃 item
"""


class DuplicatesPipeline(object):  # 去重管道

    def __init__(self):
        self.book_set = set()  # 做去重，粗暴不推荐

    def process_item(self, item, spider):
        name = item['name']
        if name in self.book_set:
            raise DropItem("Duplicate book cound: %s" % item)

        self.book_set.add(name)
        return item

class BooksInfoPipeline(object):  # 英镑转换人名币管道

    # 英镑兑换人民币汇率8.9761
    exchange_rate = 8.9761

    def process_item(self, item, spider):
        # 提取item的price字段(如£51.77)
        # 去掉签名的英镑符号，转换为float类型，乘以汇率
        item['price'] = float(item['price'][1:]) * self.exchange_rate
        item['price'] = '￥%.2f' % item['price']

        return item

class SaveInfoPipeline(object):  # 写文件管道

    def open_spider(self, spider):
        self.file = open('books_info.txt', 'w', encoding='utf-8')
        print('我打开了文件')

    def process_item(self, item, spider):
        line = '{}\n'.format(json.dumps(dict(item)))
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URL', 'mongodb://localhost:27017/')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')

        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def process_item(self, item, spider):
        collection = self.db[spider.name]  # spider.name 就爬虫类下面的name属性
        post = dict(item) if isinstance(item, Item) else item  # ???不知道 这样处理的意义，难道说返回回来的又可能是空的?
        collection.insert_one(post)
        return item

    def close_spider(self, spider):
        self.client.close()



