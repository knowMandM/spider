# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class detailMovieItem(scrapy.Item):
   name = scrapy.Field()
   descripe = scrapy.Field()
   image = scrapy.Field()
   director = scrapy.Field()
   actors = scrapy.Field()

print(detailMovieItem.__dict__.keys())