# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy import Item


class NewBooksInfosPipeline(object):
    start = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    def open_spider(self, spider):
        self.file = open('books_info.txt', 'w', encoding='utf-8')
        print('我打开文件了')

    def process_item(self, item, spider):
        start_level = self.start.get(item['starts'])
        item['starts'] = start_level
        book_info = dict(item) if isinstance(item, Item) else item
        line = '\n{}'.format(json.dumps(book_info, ensure_ascii=False))
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()
        print('关闭文件了')
