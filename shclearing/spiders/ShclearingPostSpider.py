#!/usr/bin/python
#-*- encoding:utf8 -*-
import json
import logging
import scrapy
import datetime
from shclearing.items import ShclearingPdfNews 
from scrapy.http.request.form import FormRequest

class ShclearingPostSpider(scrapy.Spider):
    name = "shclearingPostSpider"

    def start_requests(self):
        try:        
            limit = '50'
            channelId = '144'
            for start in range(1,10000):
                formdata = {'start':str(start), 'limit':limit, 'channelId':channelId}
                url = "http://www.shclearing.com/shchapp/web/disclosureForTrsServer/search"
                request_data = FormRequest(url=url, formdata=formdata, callback=self.parse_data)
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
                #从url中进一步获取pdf链接
                fileRequest = scrapy.Request(url, callback=self.parse_item) 
                fileRequest.meta['data'] = data
                yield fileRequest
        except Exception as e:  # not available site
            logging.error(e, exc_info=True)
            logging.error("Error process:")

    def parse_item(self, response):
        url = response.url
        data = response.meta.get('data')
        dom1 = response.xpath('//script/text()').re(r'fileNames = \'(.*)\'') 
        dom2 = response.xpath('//script/text()').re(r'descNames = \'(.*)\'')
        filename_arr = dom1[0].split(';;')
        downname_arr = dom2[0].split(';;')
        for index,filename in enumerate(filename_arr):
            if filename:
                item = ShclearingPdfNews()
                item['pdf_filename'] = filename[2:]
                item['pdf_downname'] = downname_arr[index]
                item['title'] = data['title']
                item['url']  = data['linkurl']                       
                tmp = url.split('/')
                item['type1'] = tmp[4]                               
                item['type2'] = tmp[5]
                item['publish_time'] = data['pubdate']
                item['create_time'] = datetime.datetime.now()
                item['update_time'] = datetime.datetime.now()
        print item
        yield item
