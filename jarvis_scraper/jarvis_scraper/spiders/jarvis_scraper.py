# -*- coding: utf-8 -*-
import scrapy
from jarvis_scraper.items import JarvisScraperItem
from jarvis_scraper.nlp.lib import should_parse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class JarvisScraperSpider(scrapy.Spider):
    name = 'jarvis_scraper'
    start_urls = ['http://www.louvre.fr/']
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    # Method for parsing items
    def parse(self, response):
        # The list of items that are found on the particular page
        items = []
        # Only extract canonicalized and unique links (with respect to the
        # current page)
        links = LinkExtractor(
            canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            url_to = link.url
            if should_parse(url_to, 0.7):
                item = JarvisScraperItem()
                item['url_to'] = link.url
                items.append(item)
            # [TODO] Process page here
            # If page seems to be a right page (RAKE algo+cosine)
            # then summarize, add to item==>Extract to CSV
        # Return all the found items
        return items
