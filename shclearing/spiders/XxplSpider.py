#!/usr/bin/python
#-*- encoding:utf8 -*-

import logging
import scrapy
import datetime
from shclearing.items import ShclearingNews 

class XxplSpider(scrapy.Spider):
    name = "xxplSpider"
    allowed_domains = ["www.shclearing.com"]
    fixed_url = 'http://www.shclearing.com/xxpl/'
    start_urls = [fixed_url]

    #回调函数。
    #处理scrapy.http.Response对象,获取资讯url，用于进一步爬取
    def parse(self, response):
        zNodes = response.xpath('//script/text()')
        ids = zNodes.xpath('//script/text()').re(r'id\:713')
        print(ids)


