import scrapy
from datetime import datetime

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['feeds.bbci.co.uk','www.bbc.co.uk']
    start_urls = ['http://feeds.bbci.co.uk/news/world/rss.xml']

    #location of json file
    custom_settings = {
        'FEED_URI': 'news.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def parse(self, response):
        news_items = response.xpath('//item')
        for news_item in news_items:
            title = news_item.xpath('.//title/text()').get()
            description = news_item.xpath('.//description/text()').get()
            link = news_item.xpath('.//link/text()').get()
            compact_link = news_item.xpath('.//guid/text()').get()
            date = news_item.xpath('.//pubDate/text()').get()

            if 'covid' in title.lower() or 'covid' in description.lower():
                converted_date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                time_delta = datetime.today() - converted_date
                if time_delta.days < 5:
                    page_to_scrape = response.urljoin(compact_link)
                    yield scrapy.Request(page_to_scrape, callback=self.parse_news)
    
    def parse_news(self,response):
        title = response.xpath('//h1[@id="main-heading"]/text()').get()
        text = ""
        paragraphs = response.xpath('//div[@data-component="text-block"]/div')
        for paragraph in paragraphs:
            if len(paragraph.xpath('.//p/text()')) > 0:
                text = text + '\n' + paragraph.xpath('.//p/text()').get()
            elif len(paragraph.xpath('.//p/b/text()')) > 0:
                text = text + '\n' + paragraph.xpath('.//p/b/text()').get()

        scraped_info = {
            'title' : title,
            'text' : text
        }

        yield scraped_info