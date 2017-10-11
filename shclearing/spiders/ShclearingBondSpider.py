#!/usr/bin/python
#-*- encoding:utf8 -*-

import logging
import scrapy
import datetime
import re
import os
import requests
from shclearing.items import ShclearingPdfNews 

class ShclearingBondSpider(scrapy.Spider):
    name = "shclearingSpider"
    allowed_domains = ["www.shclearing.com"]
    fixed_url = 'http://www.shclearing.com/xxpl/fxpl/'
    rootDir = '/data/dearMrLei/data/'
    start_urls = [fixed_url]
    maxPage = 19    # ======================更新时候用，每次循环1页==================
    for i in range(1, maxPage):
        start_urls.append(start_urls[0]+'index_'+str(i)+'.html')

    #回调函数。
    #处理scrapy.http.Response对象,获取资讯url，用于进一步爬取
    def parse(self, response):
        print(response.url)
        uls = response.xpath('//ul[re:test(@class, "list")]')
        urls = uls.xpath('.//a[contains(@href, "html")]/@href').extract()
        for index,url in enumerate(urls):
            items_url = fixed_url+urls[index][2:]
            try:
                yield scrapy.Request(items_url, callback=self.parse_item)
            except Exception as e:
                logging.error(e, exc_info=True)
                logging.error("Error process: " + response.url)

    #从资讯url中提取信息并保存 
    def parse_item(self, response):
        try:
            url = response.url
            print(url)
            tmp = url.split('/') 
            type1 = tmp[4]
            type2 = tmp[5] 
            title = response.xpath('//h1[re:test(@id,"title")]/text()').extract()[0]
            publish_time = response.xpath('//span[re:test(@class,"time")]/text()').extract()[0]
            dom1 = response.xpath('//script/text()').re(r'fileNames = \'(.*)\'') 
            dom2 = response.xpath('//script/text()').re(r'descNames = \'(.*)\'') 
            pdf_filename_arr = dom1[0].split(';;')
            pdf_downname_arr = dom2[0].split(';;')
            for index,filename in enumerate(pdf_filename_arr):
                if filename:
                    item = ShclearingPdfNews()
                    item['url'] = url
                    item['title'] = response.xpath('//h1[re:test(@id,"title")]/text()').extract()[0]
                    item['publish_time'] = ""
                    m= re.match(r".*?/t(\d{4})(\d{2})(\d{2})_(\d+).*?", url)
                    if m:
                        item['publish_time'] = m.group(1) + '-' +m.group(2) + '-' + m.group(3)
                    item['pdf_filename'] = filename[2:]
                    item['pdf_downname'] = pdf_downname_arr[index]
                    item['type1'] = type1
                    item['type2'] = type2
                    item['create_time'] = datetime.datetime.now() 
                    item['update_time'] = datetime.datetime.now() 
                    yield item
        except Exception as e:
            logging.error(e, exc_info=True)
            logging.error("Error process:" + response.url)

        def get_index_url(self):

            return 11


