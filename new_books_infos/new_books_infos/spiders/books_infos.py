# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from ..items import NewBooksInfosItem
from pyquery import PyQuery
import re


class BooksInfosSpider(scrapy.Spider):
    name = 'books_infos'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        le_rule_info = LinkExtractor(restrict_xpaths='//div[@class="image_container"]')
        le_next_page = LinkExtractor(restrict_xpaths='//li[@class="next"]')
        books_info = le_rule_info.extract_links(response)

        for book in books_info:
            yield Request(book.url, callback=self.parse_book_info, meta={'book_url': book.url})

        next_url = le_next_page.extract_links(response)[0].url
        if next_url:
            yield Request(next_url, callback=self.parse)

    def parse_book_info(self, response):
        """
        name = scrapy.Field()
        price = scrapy.Field()
        stock = scrapy.Field()
        starts = scrapy.Field()
        UPC = scrapy.Field()
        number_of_reviews = scrapy.Field()
        link = scrapy.Field()
        """
        pyq = PyQuery(response.text)

        book_infos = NewBooksInfosItem()
        book_infos['link'] = response.meta.get('book_url')
        book_infos['name'] = pyq('#content_inner > article > div.row > div.col-sm-6.product_main > h1').text()
        book_infos['price'] = pyq('#content_inner > article > div.row > div.col-sm-6.product_main > p.price_color').text()
        # 处理库存量
        stock = pyq('#content_inner > article > div.row > div.col-sm-6.product_main > p.instock.availability').text()
        book_infos['stock'] = re.findall(r'\d+', stock)[0]
        book_infos['UPC'] = pyq('#content_inner > article > table > tr:nth-child(1) > td').text()
        # 处理评星 输出 One Two Three Four Five 在管道再做变换处理
        start = pyq('#content_inner > article > div.row > div.col-sm-6.product_main > p:nth-child(4)').attr('class').split()
        book_infos['starts'] = start[1]
        book_infos['number_of_reviews'] = pyq('#content_inner > article > table > tr:nth-child(7) > td').text()
        yield book_infos


