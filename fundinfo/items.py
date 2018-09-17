# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundinfoItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    type = scrapy.Field()


class YangLeeItem(scrapy.Item):
    url = scrapy.Field()
    basic = scrapy.Field()
    additional = scrapy.Field()
