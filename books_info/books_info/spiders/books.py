# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['toscrape.com']
#    start_urls = ['http://books.toscrape.com/']
# 重写strat_requests(self): 则意味着放弃start_urls作为启动链,文档也建议我们重写

    def start_requests(self):
        yield scrapy.Request('http://books.toscrape.com',
                             callback=self.parse_book,
                             headers={'User-Agent': 'Mozilla/5.0'},
                             dont_filter=True)




    def parse_book(self, response):
        # 提取数据
        # 每一本数的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的article元素，并依次迭代
        for book in response.css('article.product_pod'):
            # 书名信息在 article>h3>a元素的title属性里
            # 例如：<a title="A Light in the Attic"> A Light in the..</a>
            name = book.xpath('./h3/a/@title').extract_first()

            # 书价信息在<p class="price_color">的TEXT中
            # 例如: <p class="price_color">£51.77</p>
            price = book.css('p.price_color::text').extract_first()
            yield {
                'name': name,
                'price': price,
            }

        # 提取链接
        # 下一页的url在ul.pager>li.next>a里面
        # 例如: <li class="next"><a href="catalogue/page-2.html">next</a></li>
        # next_url = response.css('ul.pager li.next a::attr(href)').extract_first()

        # 提取下一页的思路二，用LinkExtractor
        #  先构造匹配规则
        next_page_rule = LinkExtractor(restrict_xpaths='//li[@class="next"]')
        next_url = next_page_rule.extract_links(response)
        if next_url:
            # 如果找到下一页url，利用response.url()得到绝对路径，构造新的Request对象
            next_url = next_url[0].url
            yield scrapy.Request(next_url, callback=self.parse_book)