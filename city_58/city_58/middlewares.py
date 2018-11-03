# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent


class UAMiddleware(object):

    def process_request(self, request, spider):  # 对request进行拦截
        ua = UserAgent()  # 使用random模块，随机在ua_list中选取User-Agent
        request.headers['User-Agent'] = ua.random  # 把选取出来的User-Agent赋给request
        print(request.url)   # 打印出request的url
        print("UA:", request.headers)  # 打印出request的headers

    def process_response(self, request, response, spider):  # 对response进行拦截
        return response

    def process_exception(self, request, exception, spider):  # 对process_request方法传出来的异常进行处理
        pass
