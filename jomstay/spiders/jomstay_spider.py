# -*- coding: utf-8 -*-
import scrapy, re
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class JomstaySpiderSpider(CrawlSpider):
    name = 'jomstay_spider'
    #allowed_domains = ['libreriatemasylibros.py']
    start_urls = ['http://www.jomstay.com/']

    rules = (
    	#Rule (LinkExtractor(allow=[r'http://www.jomstay.com/category']), follow= True),
    	Rule (LinkExtractor(restrict_xpaths=('//ul[@class="page-numbers"]'), allow=[r'category/\w+']), callback='parse_start_url', follow=True),
    	)

    
    def parse_start_url(self, response):
        locations = response.css('ul.sub-menu li.menu-item')
        for location_url in locations:
            request = Request(response.urljoin(location_url.xpath('.//@href').extract_first()), callback=self.parse_details, encoding='urf-8')
            request.meta["State"] = location_url.xpath('.//text()').extract_first()

            yield request

    def parse_details(self, response):
        for item in response.css('article.genaral-post-item'):
            yield {
            "Name" : item.css('h2.genpost-entry-title > a::text').extract_first(),
            "State" : response.meta["State"],
            "Phone" : item.css('span.phone').xpath('.//a/text()').extract_first(),
            "Price" : item.css('span.rental-amount').xpath('.//a/text()').extract_first(),
            }