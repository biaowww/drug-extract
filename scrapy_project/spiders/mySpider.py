 # -*- coding: utf-8 -*-

import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy_project.items import ScrapyProjectItem

class MySpider(CrawlSpider):
	name = 'wanfang'
	allowed_domains = ['wanfangdata.com.cn']
	drugs = ['捷诺维', ]
	start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q=' + drug for drug in drugs]
	rules = [
		 Rule(LinkExtractor(allow=[start_url + '&p=\d+' for start_url in start_urls], restrict_xpaths=('//p[@pager_space]'), unique=True), callback="parse_items", follow=True), 
	]

	def parse_items(self, response):
		# self.log('Hi, this is an item page! %s' % response.url)
		items = response.xpath('//ul[@class="list_ul"]')
		for item in items:
			post = ScrapyProjectItem()  
			post['title'] = item.select('li[@class="title_li"]/a[3]/text()').extract()
			post['link'] = item.select('li[@class="title_li"]/a[3]/@href').extract()
			yield post

