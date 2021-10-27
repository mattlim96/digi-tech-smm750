import scrapy
import scrapy_splash

class AmzSpider(scrapy.Spider):
    name = 'amz'
    allowed_domains = ['www.amazon.co.uk']

    #location of json file
    custom_settings = {
        'FEED_URI': 'amz.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    def start_requests(self):
        url = 'https://www.amazon.co.uk/gp/deals/?ie=UTF8&pd_rd_w=4wGbI&pf_rd_p=346c6136-7bc4-49af-8040-6ff24d6ad1c7&pf_rd_r=RMPYZDTBV62JG8PZJDGP&pd_rd_r=7c0634c5-d977-4970-b817-e858b72e99c5&pd_rd_wg=HTY0f&ref_=pd_gw_unk'
        
        # Instead of a the original scrapy.Request, we use scrapy_splash.SplashRequest here!
        yield scrapy_splash.SplashRequest(  url=url,
                                            callback=self.parse,
                                            args = {'wait': 3}  )

    def parse(self, response):
        items = response.xpath('//div[contains(@class,"DealGridItem-module__dealItemContent")]/div')
        for item in items:
            title = item.xpath('.//a/div[contains(@class,"DealContent-module")]/text()').get()
            prices = item.xpath('.//span[@class="a-price-whole"]/text()').getall()
            ending = item.xpath('.//div[@class="a-row a-spacing-mini a-spacing-top-mini"]/span/span/text()').get()
            if title != None:
                yield {
                    'title' : title,
                    'lower_price' : str(min([float(s) for s in prices])),
                    'upper_price' : str(max([float(s) for s in prices])),
                    'ending' : ending
                }


