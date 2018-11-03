# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from ..items import JDItem

# 爬取京东自营图书，


lua_script = '''
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementById('footer-2017').scrollIntoView()")
    splash:wait(2)
    return splash:html()
end
'''


class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    base_url = 'https://search.jd.com/Search?keyword=python&enc=utf-8&wq=python&wtype=1'

    def start_requests(self):
        yield SplashRequest(url=self.base_url,
                            args={'lua_source': lua_script},
                            callback=self.parse_url,
                            endpoint='execute',)


    def parse_url(self, response):
        # 获取商品总数，计算出总页数 &page=1
        total_page = int(response.css('div#J_bottomPage > span.p-skip b::text').extract_first())
        print('总共有%d页' % total_page)
        for page in range(total_page):
            url = self.base_url + '&page={}'.format(2*page+1)
            yield SplashRequest(url=url,
                                callback=self.parse,
                                endpoint='execute',
                                args={'lua_source': lua_script},
                                cache_args=['lua_source'])


    def parse(self, response):
        # 获取每一个页面中每本书的名字和价格
        for sel in response.css('li.gl-item'):
            book_infos = JDItem()
            book_infos['name'] = sel.css('div.p-name').xpath('string(.//em)').extract_first()
            book_infos['price'] = sel.css('div.p-price > strong i::text').extract_first()
            book_infos['desc'] = sel.xpath('./div/div[3]/a/@title').extract_first()
            book_infos['author'] = sel.xpath('./div/div[4]/span[1]/a[1]/@title').extract_first()
            yield book_infos

