# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
import sys
sys.path.append('.')
from scrapy_test import settings

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['douban.com/']
    start_urls = [r'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=100&page_start=0']

    def parse(self, response):
        with open(settings.JSON_FILE, "w") as f:
            f.write(response.text)
