# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import open_in_browser
from fundinfo.items import FundinfoItem
from scrapy.shell import inspect_response
from fundinfo.spiders import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from fundinfo.items import YangLeeItem
from selenium.common.exceptions import StaleElementReferenceException


class YangLee(scrapy.Spider):
    name = "yanglee"
    # allowed_domains = ["www.amac.org.cn"]
    # start_urls = ['http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html']
    start_urls = ['http://www.yanglee.com/Product/Index.aspx']
    driver = driver
    driver.implicitly_wait(10)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'use_js': '123'}, callback=self.parse)

    def process_page(self, response):
        # 点击在售
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="procon1"]/li[1]/div/span[2]/div/label/span[2]')))

        element.click()

        count = 1
        finished = False
        while not finished:
            # 等待点击之后的页面刷新
            WebDriverWait(self.driver, 3).until(EC.staleness_of(self.driver.find_element_by_css_selector('.block')))

            for ele in self.driver.find_elements_by_css_selector('.block'):
                url = response.urljoin(ele.get_attribute('href'))
                yield scrapy.Request(url, callback=self.parse_detail)

            element = self.driver.find_element_by_css_selector('.pagination .next')

            if 'disabled' in element.get_attribute('class'):
                finished = True

            print("爬取第{}页".format(count))
            self.driver.execute_script("arguments[0].click();", element)
            count += 1

    def parse(self, response):

        # 爬取信托产品数据
        for item in self.process_page(response):
            yield item

        job_list = {
            '资管产品': '//*[@id="radpro2"]/label/e',
            '私募产品': '//*[@id="pro_type"]/span[3]/div/label/e',
            # '其它产品': '//*[@id="pro_type"]/span[4]/div/label/e'
        }

        # 依次爬取其他类别数据
        for key, val in job_list.items():
            print("爬取{}页面数据".format(key))
            self.driver.find_element_by_xpath(val).click()
            time.sleep(1)
            for item in self.process_page(response):
                yield item

    def parse_detail(self, response):
        keys = response.css('#procon1 td:not(.pro-textcolor) *::text').extract()
        values = response.css('#procon1 td.pro-textcolor *::text').extract()
        basic = dict(zip(keys, values))

        additional = {info.css('h1::text').extract_first(): info.css('p::text').extract() for info in
                      response.css('div:not(#wbox).wbox')}

        yield YangLeeItem(url=response.url, basic=basic, additional=additional)
