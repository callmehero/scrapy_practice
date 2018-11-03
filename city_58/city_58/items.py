# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class City58Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    detail_link = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    house_detail = scrapy.Field()
    location = scrapy.Field()
    location_detail = scrapy.Field()
