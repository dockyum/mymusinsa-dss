
import scrapy
from image.items import ImageItem
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Image"
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

    def __init__(self, midcode="001001", page="1"):
        self.start_urls = [f"https://search.musinsa.com/category/{midcode}?page={page}/"]
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        links = response.xpath('//*[@id="searchList"]/li/div[contains(@class,"li_inner")]/div[2]/p[2]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)
            
    def parse_content(self, response):
        item = ImageItem()
        item["img_link"] = "https:" + response.xpath('//*[@id="detail_bigimg"]/div[1]/img/@src')[0].extract()
        item["item_id"] = response.url.split('/')[-1]
        
        yield item
