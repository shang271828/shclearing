#!/usr/bin/python
#-*- encoding:utf8 -*-
#获取上海清算网的债券目录结构，存入数据库表shclearing_xxpl_map
import logging
import scrapy
import datetime
from shclearing.items import xxplItem  

class XxplSpider(scrapy.Spider):
    name = "xxplSpider"
    allowed_domains = ["www.shclearing.com"]
    fixed_url = 'http://www.shclearing.com/xxpl/'
    start_urls = [fixed_url]

    #回调函数。
    #处理scrapy.http.Response对象,获取资讯url，用于进一步爬取
    def parse(self, response):
        ids = response.xpath('//script/text()').re(r'id\:(\d+)')
        pIds = response.xpath('//script/text()').re(r'pId\:(\d+)')
        names = response.xpath('//script/text()').re(r'name\:"(.*)",xxpl_url')
        xxpl_urls = response.xpath('//script/text()').re(r'xxpl_url\:"\.(.*)",xxpl_id')
        xxpl_ids = response.xpath('//script/text()').re(r'xxpl_id\:"(.*)",xxpl_desc')
        xxpl_descs = response.xpath('//script/text()').re(r'xxpl_desc\:"(.*)"}')

        for index,sh_id in enumerate(ids): 
            item = xxplItem()
            item['sh_id'] = sh_id
            item['pId'] = pIds[index]
            item['name'] = names[index]
            item['xxpl_url'] = xxpl_urls[index]
            item['xxpl_id'] = xxpl_ids[index]
            item['xxpl_desc'] = xxpl_descs[index]
            url = self.fixed_url[:-1] + item['xxpl_url']
            yield scrapy.Request(url, meta={'item': item}, callback=self.parse_item) 

    def parse_item(self,response):
        url = response.url
        channel_id = response.xpath('//div[contains(@class, "page_roll")]').re(r'chnlId : (\d+)')
        item = response.meta['item']
        item['channel_id'] = channel_id[0]
        yield item
