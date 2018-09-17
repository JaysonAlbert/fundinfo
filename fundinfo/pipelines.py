# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from fundinfo.items import YangLeeItem


class YangLeePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, YangLeeItem):
            item_dict = item['basic']
            item_dict.update(item['additional'])
            item_dict['url'] = item['url']
            return item_dict
        else:
            return item
