
import scrapy
from scrapy.http import TextResponse
from sizeinfo.items import SizeinfoItem
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Sizeinfo"
    allow_domain = ["musinsa.com"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
    #         'DOWNLOAD_DELAY': 2.0,
        'AUTOTHROTTLE_ENABLED': True,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
            'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        }
    }
    
    def __init__(self, mid_code="001001", **kwargs):
        self.start_urls = [f"https://search.musinsa.com/category/{mid_code}"]
        super().__init__(**kwargs)
        
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        link = response.xpath('//*[@id="searchList"]/li[1]/div[3]/div[1]/a/@href')[0].extract()
        yield scrapy.Request(link, callback=self.parse_content)
        
    def parse_content(self, response):
        item = SizeinfoItem()
        si = response.xpath('//*[@id="size_table"]/thead/tr/th[contains(@class, "item_val")]/text()').extract()
        item["size_info"] = []
        for idx in range(len(si)):
            if idx % 2 != 0:
                item["size_info"].append(si[idx].strip())
        yield item
