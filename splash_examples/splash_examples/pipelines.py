# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import re
from scrapy.item import Item
import pymongo


class SplashExamplesPipeline(object):
    re_com = re.compile(r'“(.*)”')

    def open_spider(self, spider):
        self.file = open('quotes_info.txt', 'w', encoding='utf-8')
        print('我打开了文件')

    def process_item(self, item, spider):
        if isinstance(item, dict):
            # “To die will be an awfully big adventure.”
            item['quote'] = self.re_com.match(item['quote']).group(1)
            line = '{}\n'.format(json.dumps(dict(item), ensure_ascii=False))
            self.file.write(line)

        return item

    def close_spider(self, spider):
        self.file.close()
        print('我关闭文件了')


class JDbooksPipeline(object):

    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017/')   # 会去settings.py中去寻找  'MONGO_DB_URL' 要连接MONGODB的地址，如果没有则默认连接 'mongodb://localhost:27017/'
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')  # 回去settings.py中寻找，'MONGO_DB_NAME' 要连接数据库的名，如果没有则默认连接 'scrapy_data'

        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def process_item(self, item, spider):
        collection = self.db[spider.name] # spider.name 就爬虫类下面的name属性
        post = dict(item) if isinstance(item, Item) else item # ???不知道 这样处理的意义，难道说返回回来的又可能是空的?
        collection.insert_one(post)
        return item

    def close_spider(self, spider):
        self.client.close()