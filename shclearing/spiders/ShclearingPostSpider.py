#!/usr/bin/python
#-*- encoding:utf8 -*-
import json
import logging
import scrapy
import datetime
from shclearing.items import ShclearingNews
from scrapy.http.request.form import FormRequest

class ShclearingPostSpider(scrapy.Spider):
    name = "shclearingPostSpider"
#    allowed_domains = ["www.shclearing.com"]
#    fixed_url = 'http://www.shclearing.com/xxpl/fxpl/'
#    start_urls = [fixed_url]

    def start_requests(self):
        try:        
            start = '0'
            limit = '20'
            channelId = '144'
            formdata = {'start':start, 'limit':limit, 'channelId':channelId}
            url = "http://www.shclearing.com/shchapp/web/disclosureForTrsServer/search"
            request_data = FormRequest(url=url, formdata=formdata, callback=self.parse_data)
            request_data.meta['pageNum'] = 1
            request_data.meta['sourceType'] = 10
            yield request_data
        except Exception as e:
           logging.error(e, exc_info=True) 
           logging.error("Error process: ")
    def parse_data(self, response):
        result_json_string = response.body_as_unicode()
        try:
            result_json = json.loads(result_json_string)
            datas_json = result_json['datas']
            for data in datas_json:
                url = data['linkurl'] 
                scrapy.Request(url, callback=self.parse_item) 
                tmp = url.split('/') 
                type1 = tmp[4] 
                type2 = tmp[5]
                item = ShclearingNews()
                item['title'] = data['title']
                item['url']  = data['linkurl']

                item['type1'] = type1
                item['type2'] = type2
                item['publish_time'] = data['pubdate']
                item['create_time'] = datetime.datetime.now()
                item['update_time'] = datetime.datetime.now()
                print(item)
                yield item 
        except Exception as e:  # not available site
            logging.error(e, exc_info=True)
            logging.error("Error process:")

    def parse_item(self, response):
       url = response.url
       print(111)
       print(url)
