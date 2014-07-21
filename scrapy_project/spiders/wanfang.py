# -*- coding: utf-8 -*-

import urllib
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request

from scrapy_project.items import ScrapyProjectItem

def get_drugs():
    f = open('drugs.txt', 'r')
    s = f.readlines()
    f.close()

    drugs = []
    for line in s:
        if line not in drugs:
            drugs.append(line)
    return drugs

class MySpider(CrawlSpider):
    name = 'wanfang'
    allowed_domains = ['wanfangdata.com.cn']
    drugs = get_drugs()
    start_urls = ['http://s.wanfangdata.com.cn/Paper.aspx?q='+urllib.quote(' '.join(drugs)), ]
    rules = [
            Rule(LinkExtractor(restrict_xpaths=('//ul[@class="list_ul"]/li[@class="title_li"]/a[3]'), unique=True), callback="parse_items", follow=False),
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
        post['institutes'] = []

        for item in items:
            print "_"*80 + "\n", item.extract()
               
            content = u""
            if item.xpath('./th/t'):
                content = item.xpath('./th/t/text()').extract()[0]
            '''
            # get a link for next page
            next_page = hxs.xpath('//p[@class="pager_space"]/a')
            next_page_link = u""
            for link in next_page:
                if link.xpath('t/text()').extract() == []:
                    pass
                elif link.xpath('t/text()').extract()[0] == u'\u4e0b\u4e00\u9875':
                    next_page_link = link.xpath('@href').extract()   
            '''
            ###    extract authors' names
            if content == u'\u4f5c\u8005':
                _authors = item.xpath('./td/a')
                for _author in _authors:
                    author = _author.xpath('./text()').extract()[1].replace(' ', '').replace('\r\n', '')
                    post['authors'].append(author)
                continue
            ###    extract institutes information
            elif content == u'\u4f5c\u8005\u5355\u4f4d':
                if item.xpath('./td/ol/li'): 
                    _institutes = item.xpath('./td/ol/li')
                    for _institue in _institutes:
                        institute = _institue.xpath('./text()').extract()[0].replace(' ', '').replace('\r\n', '')
                        post['institutes'].append(institute)
                else: 
                    institute = item.xpath('./td/text()').extract()[0].replace(' ', '').replace('\r\n', '') 
                    post['institutes'].append(institute)
            ###    extract journal name and volume number     
            elif content == u'\u520a  \u540d\uff1a':
                post['journal'] = item.xpath('./td/a/text()').extract()[0].replace(' ', '').replace('\r\n', '')
            elif content == u'\u5e74\uff0c\u5377\u0028\u671f\u0029':
                post['volume'] = item.xpath('./td/a/text()').extract()[0].replace(' ', '').replace('\r\n', '')
            ###    extract keywords    
            elif content == u'\u5173\u952e\u8bcd\uff1a':
                _keywords = item.xpath('./td/a')    
                for _keyword in _keywords:
                    if _keyword.xpath('./text()').extract():
                        keyword = _keyword.xpath('./text()').extract()[0].replace(' ', '').replace('\r\n', '')
                        post['keywords'].append(keyword)
                while u'' in post['keywords']: post['keywords'].remove(u'')    
                continue
            else:
                continue
        yield post

