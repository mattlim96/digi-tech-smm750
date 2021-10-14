import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-page{page}.json'
        quote_list = []
        for quote in response.xpath('//div[@class="quote"]'):
            quote_dict = {
                'text': quote.xpath('.//span[@class="text"]/text()').get(),
                'author': quote.xpath('.//small[@class="author"]/text()').get(),
                'tags': quote.xpath('.//a[@class="tag"]/text()').getall()
            }
            quote_list.append(quote_dict)
        with open(filename, 'w') as f:
            json.dump(quote_list , f)
        self.log(f'Saved file {filename}')