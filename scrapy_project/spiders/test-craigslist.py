import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy_project.items import ScrapyProjectItem

class MySpider(CrawlSpider):
	name = 'craigslist'
	allowed_domains = ['craigslist.org']
	start_urls = ['http://sfbay.craigslist.org/npo/']
	rules = [
		 Rule(LinkExtractor(allow=('npo/index\d00\.html'), restrict_xpaths=('//span[@class="buttons"]')), callback="parse_items", follow=True), 
	]

	def parse_items(self, response):
		# self.log('Hi, this is an item page! %s' % response.url)
		items = response.xpath('//div[@class="content"]/p')
		for item in items:
			post = ScrapyProjectItem()  
			post['title'] = item.select('span[@class="pl"]/a/text()').extract()
			post['link'] = item.select('span[@class="pl"]/a/@href').extract()
			yield post

