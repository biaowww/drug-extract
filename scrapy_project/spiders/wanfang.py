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
	print start_urls;
	rules = [
	 	 # Rule(LinkExtractor(restrict_xpaths=('//p[@class="pager_space"]'), unique=True), callback="parse_items", follow=True), 
		   Rule(LinkExtractor(allow=['Paper.aspx\?q=' + drug + '&p=\d+' for drug in drugs], restrict_xpaths=('//p[@class="pager_space"]'), unique=True), callback="parse_items", follow=True), 

	]

	def parse_items(self, response):
		# print "Zzzzzzzzzzzzzz"
		# self.log('Hi, this is an item page! %s' % response.url)
		items = response.xpath('//ul[@class="list_ul"]')
		for item in items:
			post = ScrapyProjectItem()  
			post['title'] = item.select('li[@class="title_li"]/a[3]/text()').extract()
			post['link'] = item.select('li[@class="title_li"]/a[3]/@href').extract()
			yield post

