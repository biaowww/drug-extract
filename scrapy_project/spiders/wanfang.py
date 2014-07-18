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
            Rule(LinkExtractor(allow=('http://d\.wanfangdata\.com\.cn/Periodical_\w+\d+\.aspx'), restrict_xpaths=('//ul[@class="list_ul"]'), unique=True), callback="parse_items", follow=False),
            Rule(LinkExtractor(restrict_xpaths=('//p[@class="pager_space"]'), unique=True), follow=True), 
            # Rule(LinkExtractor(allow=('\?q='+drug+'&p=\d+' for drug in drugs), restrict_xpaths=('//p[@class="pager_space"]'), unique=True), callback="parse_items", follow=True), 
    ]

    def parse_items(self, response):
        # self.log('Hi, this is an item page! %s' % response.url)

        '''
        items = response.xpath('//ul[@class="list_ul"]')
        items = response.xpath('//h1')
        for item in items:
            post = ScrapyProjectItem()  
            # post['title'] = item.xpath('li[@class="title_li"]/a[3]/text()').extract()
            # post['link'] = item.xpath('li[@class="title_li"]/a[3]/@href').extract()
            post['title'] = item.xpath('text()').extract()
            yield post
         '''
        post = ScrapyProjectItem()
        post['title'] = response.xpath('//h1/text()').extract()[0].replace(' ', '').replace('\r\n', '')
        if response.xpath('//dl[@class="abstract_dl"]/dd/text()').extract():
            post['abstract'] = response.xpath('//dl[@class="abstract_dl"]/dd/text()').extract()[0].replace(' ', '').replace('\r\n', '')
         
        items = response.xpath('//div[@id="detail_leftcontent"]//table/tr')

        post['authors'] = []
        post['keywords'] = []

        for item in items:
            print "_"*80, item.extract()
               
            content = u""
            if item.xpath('./th/t'):
                content = item.xpath('./th/t/text()').extract()[0]
               
            # print "+"*80, item.xpath('./th/t/text()').extract()
            # print "*"*80, content == u'\u5173\u952e\u8bcd\uff1a'

            if content == u'\u4f5c\u8005':
                _authors = item.xpath('./td/a')    ### extract authors information
                for _author in _authors:
                    author = _author.xpath('./text()').extract()[1].replace(' ', '').replace('\r\n', '')
                    post['authors'].append(author)
                continue
            elif content == u'\u5173\u952e\u8bcd\uff1a':
                _keywords = item.xpath('./td/a')    ###	extract keywords
                for _keyword in _keywords:
                    if _keyword.xpath('./text()').extract():
                        keyword = _keyword.xpath('./text()').extract()[0].replace(' ', '').replace('\r\n', '')
                        post['keywords'].append(keyword)
                while u'' in post['keywords']: post['keywords'].remove(u'')    
                continue
            else:
                continue
        yield post

