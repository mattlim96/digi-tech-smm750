import scrapy
import json

class NewsSpider(scrapy.Spider):
    #name of the spider
    name = 'news'

    #location of json file
    custom_settings = {
        'FEED_URI': 'news.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    #list of allowed domains
    allowed_domains = ['feeds.bbci.co.uk','www.bbc.co.uk']

    #starting url for scraping
    start_urls=['http://feeds.bbci.co.uk/news/world/rss.xml',]

    def parse(self, response):

        news_urls = []

        ### FINDING THE CORRECT URLS
        
        for url in news_urls:
            yield {'url' : news_urls}