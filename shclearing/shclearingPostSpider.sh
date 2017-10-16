#!/bin/bash

cd /root/apps/scrapy/shclearing/
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl shclearingPostSpider

