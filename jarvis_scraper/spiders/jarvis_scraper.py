# -*- coding: utf-8 -*-
import operator

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from jarvis_scraper.items import JarvisScraperItem
from jarvis_scraper.nlp.lib import get_distance


class JarvisScraperSpider(scrapy.Spider):
    name = 'jarvis_scraper'
    start_urls = ['http://www.musee-armee.fr']
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
        items = []
        # The list of items that are found on the particular page
        url_distance = {}
        # Only extract canonicalized and unique links (with respect to the
        # current page)
        links = LinkExtractor(
            canonicalize=True, unique=True).extract_links(response)
        # Now go through all the found links
        for link in links:
            url_to = link.url
            distance = get_distance(url_to)
            url_distance[url_to] = distance
            # Get url with best content matches based on Cosine distance
        best_url_matches = dict(
            sorted(url_distance.items(), key=operator.itemgetter(1),
                   reverse=True)[:5])
        for url in best_url_matches:
            item = JarvisScraperItem()
            item['url_to'] = url
            items.append(item)
        return items
