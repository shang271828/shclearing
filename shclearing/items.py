# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShclearingNews(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    publish_time = scrapy.Field()
    channel_url = scrapy.Field()
    channel_name = scrapy.Field()
    channel_id = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()

class ShclearingPdfNews(ShclearingNews):
    # define the fields for your item here like:
    pdf_filename = scrapy.Field()
    pdf_downname = scrapy.Field()
  
class xxplItem(scrapy.Item):
    sh_id = scrapy.Field()
    pId = scrapy.Field()
    xxpl_url = scrapy.Field()
    name = scrapy.Field()
    xxpl_id = scrapy.Field()
    xxpl_desc = scrapy.Field()
    channel_id = scrapy.Field()
