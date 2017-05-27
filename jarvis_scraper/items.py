# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JarvisScraperItem(scrapy.Item):
    url_to = scrapy.Field()
    summarized_text = scrapy.Field()
    pass
