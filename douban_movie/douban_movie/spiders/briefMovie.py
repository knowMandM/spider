# -*- coding: utf-8 -*-
import scrapy
import sys, json
sys.path.append('.')
from douban_movie import settings


class BriefmovieSpider(scrapy.Spider):
    name = 'briefMovie'
    allowed_domains = ['douban.com/']
    start_urls = [r'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=101&page_start=0']

    def parse(self, response):
        json.dump(json.loads(response.text), open(settings.JSON_FILE, "w"), ensure_ascii=False)