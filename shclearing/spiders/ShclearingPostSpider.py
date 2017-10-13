#!/usr/bin/python
#-*- encoding:utf8 -*-
import json
import logging
import scrapy
import datetime
from shclearing.items import ShclearingPdfNews 
from scrapy.http.request.form import FormRequest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import CHAR, Integer, String

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'shclearing_xxpl_map'
    id  = Column(Integer, primary_key=True)
    channel_id = Column(Integer)
    xxpl_desc = Column(String)
    xxpl_url = Column(String)
    pId = Column(String)

class ShclearingPostSpider(scrapy.Spider):
    name = "shclearingPostSpider"

    def start_requests(self):
        try:        
            limit = '100'
            xxpl_map = self.get_channel()
            for xxpl_item in xxpl_map:
                channel_id = xxpl_item.channel_id
                for start in range(1,1000):
                    formdata = {'start':str(start), 'limit':limit, 'channelId':str(channel_id)}
                    url = "http://www.shclearing.com/shchapp/web/disclosureForTrsServer/search"
                    request_data = FormRequest(url=url, formdata=formdata, callback=self.parse_data)
                    request_data.meta['xxpl_item'] = xxpl_item
                    yield request_data
        except Exception as e:
           logging.error(e, exc_info=True) 
           logging.error("Error process: ")

    def parse_data(self, response):
        result_json_string = response.body_as_unicode()
        try:
            result_json = json.loads(result_json_string)
            if result_json.has_key('datas'):
                datas_json = result_json['datas']
                for data in datas_json:
                    url = data['linkurl'] 
                    #从url中进一步获取pdf链接
                    fileRequest = scrapy.Request(url, callback=self.parse_item) 
                    fileRequest.meta['data'] = data
                    fileRequest.meta['xxpl_item'] = response.meta.get('xxpl_item')
                    yield fileRequest
        except Exception as e:  # not available site
            logging.error(e, exc_info=True)
            logging.error("Error process:")

    def parse_item(self, response):
        url = response.url
        print(url)
        data = response.meta.get('data')
        xxpl_item = response.meta.get('xxpl_item')
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
                item['channel_url'] = xxpl_item.xxpl_url                               
                item['channel_name'] = xxpl_item.xxpl_desc
                tmp = xxpl_item.xxpl_url.split('/')
                item['f_type'] = tmp[1]
                item['channel_id'] = xxpl_item.channel_id
                item['publish_time'] = data['pubdate']
                item['create_time'] = datetime.datetime.now()
                item['update_time'] = datetime.datetime.now()
                yield item

    def get_channel(self):
        result = []
        try:
            engine = create_engine('mysql://root:hoboom@106.75.3.227:3306/scrapy?charset=utf8', echo=True)
            session = sessionmaker(bind=engine)()
            result = session.query(Channel).filter(Channel.pId!=0).all()
        except Exception as e:
            logging.error(e, exc_info=True)
        return result 
