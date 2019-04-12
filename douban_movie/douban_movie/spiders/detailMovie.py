# -*- coding: utf-8 -*-
import scrapy
import sys, json
sys.path.append('.')
from douban_movie import settings
from douban_movie import myxpath
from douban_movie.items import detailMovieItem

class DetailmovieSpider(scrapy.Spider):
    name = 'detailMovie'
    allowed_domains = ['douban.com']
    start_urls = []

    def parse(self, response):
        #with open("aaa.html", "w", encoding="utf-8") as f:
        #    f.write(response.text)
        item = detailMovieItem()
        item["name"] = myxpath.myXpath(response, '//*[@id="content"]/h1/span[1]/text()') # 电影名
        item["descripe"] = ' '.join(response.xpath(r'//*[@id="link-report"]/span/text()').extract()) # 简介
        item["image"] = myxpath.myXpath(response, '//*[@id="mainpic"]/a/img/@src') # 海报
        item["director"] = myxpath.myXpath(response, '//*[@id="info"]/span[1]/span[2]/a/text()') # 导演
        item["actors"] = repr(response.xpath(r'//a[@rel="v:starring"]/text()').extract()[:5]) # 主演
        return item

    def start_requests(self):
        # 模拟登陆
        jsonObj = json.load(open(settings.JSON_FILE, "r"))
        for each in jsonObj["subjects"]:
            if '3095514' in each["url"]: # 这部影片没有详情的，无语...
                continue
            yield scrapy.http.Request(each["url"], dont_filter=True)
