# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ExplaraItem(scrapy.Item):
	event_name = scrapy.Field()
	description = scrapy.Field()
	price = scrapy.Field()
	pass
