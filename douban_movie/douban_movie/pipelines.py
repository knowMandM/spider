# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from douban_movie import write_mysql

class DoubanMoviePipeline(object):
    def process_item(self, item, spider):
        item["descripe"] = item["descripe"].replace('\n', '').replace('                                                                                                                   　　', '                                　　')
        write_mysql.insertValue(item)
        return item
