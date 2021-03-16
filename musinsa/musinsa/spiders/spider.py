
import scrapy, re
from musinsa.items import MusinsaItem
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Musinsa"
    allow_domain = ["musinsa.com"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
    #         'DOWNLOAD_DELAY': 2.0,
        'AUTOTHROTTLE_ENABLED': True,
    #         "DOWNLOADER_MIDDLEWARES": {
    #             "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    #             'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    #             "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    #             'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    #         },
    }

    def __init__(self, midcode="001001", page="1"):
        self.start_urls = [f"https://search.musinsa.com/category/{midcode}?page_kind=search&list_kind=small&sort=new&page={page}&display_cnt=90"]
        super().__init__()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)
            
    def parse(self, response):
        links = response.xpath('//*[@id="searchList"]/li/div[contains(@class,"li_inner")]/div[1]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)
            
    def parse_content(self, response):
        item = MusinsaItem()
        title = response.xpath('/html/head/title/text()')[0].extract().split(' -')[0]
        item["title"] = title.split(') ')[-1]
        try:
            item["brand"] = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[1]/p[2]/strong/a/text()')[0].extract()
        except:
            item["brand"] = response.xpath('//*[@id="product_order_info"]/h2')
        try:
            item["o_price"] = response.xpath('//*[@id="normal_price"]/text()')[0].extract().strip()
        except:
            o_price = response.xpath('//*[@id="goods_price"]/del/text()')[0].extract().strip()
            item["o_price"] = o_price.replace(',','').split('원')[0]
        try:
            s_price = response.xpath('//*[@id="sPrice"]/ul/li/span[2]/text()')[0].extract()
            item["s_price"] = s_price.replace(',','').split('원')[0]
        except:
            item["s_price"] = item["o_price"]
        kw = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[contains(@class, "article-tag-list")]/p/a/text()').extract()
        kw = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[contains(@class, "article-tag-list")]/p/a/text()').extract()
        kw = list(map(lambda s : s.replace("#",''), kw))
        item["kw"] = ','.join(kw)
        item["img_link"] = "https:" + response.xpath('//*[@id="detail_bigimg"]/div[1]/img/@src')[0].extract()
        item["link"] = response.url
        item["item_id"] = item["link"].split('/')[-1]
        
        yield item
