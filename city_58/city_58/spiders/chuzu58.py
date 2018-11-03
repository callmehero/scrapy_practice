# -*- coding: utf-8 -*-
import scrapy
from pyquery import PyQuery
from ..items import City58Item


class ChuZu58Spider(scrapy.Spider):
    name = 'ChuZu58'
    allowed_domains = ['58.com']
    start_urls = ['https://zs.58.com/chuzu/']

    def parse(self, response):
        pyq_object = PyQuery(response.text)
        li_tags = pyq_object('body > div.mainbox > div > div.content > div.listBox > ul > li').items()
        for li in li_tags:
            if li.attr('id') == 'bottom_ad_li':
                break
            else:
                a_tag = li('div.des > h2 > a')
                items = City58Item()
                items['name'] = a_tag.text()
                items['detail_link'] = a_tag.attr('href')
                items['price'] = li('div.listliright > div.money > b').text()
                items['house_detail'], items['area'] = li('div.des > p.room.strongbox').text().split()
                items['location'] = li('div.des > p.add > a:nth-child(1)').text()
                items['location_detail'] = li('div.des > p.add > a:nth-child(2)').text().replace('...', '')  # 去掉3个恶心的点
                yield items

        next_url = pyq_object('#bottom_ad_li > div.pager > a.next').attr('href')
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse,
                                 meta={'dont_redirect': True},
                                 dont_filter=True)

