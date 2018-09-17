# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import fundinfo
from scrapy.utils.response import open_in_browser
from fundinfo.spiders import driver

import time
from scrapy.http import HtmlResponse
from fundinfo.items import FundinfoItem
from scrapy.shell import inspect_response


class FundSpider(scrapy.Spider):
    name = "fund"
    # allowed_domains = ["www.amac.org.cn"]
    start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html']
    # start_urls = ['http://gs.amac.org.cn/']

    meta = {"use_js": 999}

    handle_httpstatus_list = [304]
    driver = driver

    def parse(self, response):
        self.driver.implicitly_wait(10)
        # print(response.xpath("/html/body/div/div[2]/div/table/tbody/tr[6]/td[2]"))
        info = response.xpath("/html/body/div/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/a/text()").extract()
        url = response.xpath("/html/body/div/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/a/@href").extract_first()
        next_page = response.urljoin(url)

        yield scrapy.Request(next_page, meta=self.meta, callback=self.parse_fund)

    def parse_fund(self, response):
        time.sleep(5)
        element = self.driver.find_element_by_xpath('/html/body/div[6]/div[3]/div/button/span')
        element.click()
        element = self.driver.find_element_by_xpath('//*[@id="fundlist_paginate"]/a[4]')
        element.click()

        while True:
            time.sleep(1)
            elements = self.driver.find_elements_by_xpath('//*[@id="fundlist"]/tbody/tr/td[2]/a')
            times = [e.text for e in self.driver.find_elements_by_xpath('//*[@id="fundlist"]/tbody/tr/td[6]')]

            urls = [ele.get_attribute('href') for ele in elements]

            for url in urls:
                yield scrapy.Request(url, meta=self.meta, callback=self.parse_page)

            self.driver.find_elements_by_xpath('//*[@id="fundlist_paginate"]/a[2]').click()

    def parse_page(self, response):
        print(response.body)
