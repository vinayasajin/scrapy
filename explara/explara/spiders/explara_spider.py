# -*- coding: utf-8 -*-
import scrapy
from explara.items import *
from scrapy.http import Request, FormRequest


class ExplaraSpiderSpider(scrapy.Spider):
	name = "explara_spider"
	allowed_domains = ["explara.com"]
	start_urls = [
		'https://in.explara.com/kochi/entertainment',
	]
	page_number = 1

	def parse(self, response):
		event_links = response.xpath(
			'//div[@id="all_id_events_entertainment"]/a/@href | //div[@id="id_events_entertainment"]/a/@href | //body/a/@href').extract()
		if 'javascript' in event_links[0]:
			event_links = ''
		if event_links:
			for link in event_links:
				yield Request(link, callback=self.parse_event)
			self.page_number = self.page_number + 1
			next_page_url = 'https://in.explara.com/application/experience/load-more-events'
			frm_data = {'category': 'entertainment', 'topic': '',
						'city': 'kochi', 'country': 'India', 'page': str(self.page_number), }
			yield FormRequest(next_page_url, formdata=frm_data, method='POST', callback=self.parse)
		pass
	def parse_event(self, response):
		event_name = response.xpath(
			'//div[@itemprop="name"]//text()').extract()
		if event_name:
			event_name = ''.join(event_name).split()
			event_name = ' '.join(event_name)
		else:
			event_name = ''
		description = response.xpath(
			'//div[@id="event-description"]//div[@class="col-xs-12 description"]//text()').extract()
		if description:
			description = ''.join(description).split()
			description = ' '.join(description)
		else:
			description = ''
		price = response.xpath(
			'//div[@id="price"]/span[@style="text-transform:none;"]/text()').extract()
		if price:
			price = price[0].strip()
			price = price.replace('\n', '')
		else:
			price = ''
		if 'Free' in price:
			price=''
			pass

		item = ExplaraItem()
		item['event_name'] = event_name
		item['description'] = description
		item['price'] = price
		yield item

