
import scrapy
from musinsa.items import MusinsaItem
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Musinsa"
    allow_domain = ["musinsa.com"]
    start_urls = ["https://search.musinsa.com/category/001003"]
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
    
    def parse(self, response):
        links = response.xpath('//*[@id="searchList"]/li/div[contains(@class,"li_inner")]\
/div[2]/p[2]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)
            
    def parse_content(self, response):
        item = MusinsaItem()
        title = response.xpath('/html/head/title/text()')[0].extract().split(' -')[0]
        item["title"] = title.split(') ')[1]
        item["brand"] = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[1]/p[2]/strong/a/text()')[0].extract()
        try:
            item["o_price"] = response.xpath('//*[@id="goods_price"]/del/text()')[0].extract().strip()
        except:
            item["o_price"] = response.xpath('//*[@id="goods_price"]/text()')[0].extract().strip()
        try:
            item["s_price"] = response.xpath('//*[@id="sale_price"]/text()')[0].extract().strip()
        except:
            item["s_price"] = item["o_price"]
        kw = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[contains(@class, "article-tag-list")]/p/a/text()').extract()
        item["kw"] = list(map(lambda s : s.replace("#",''), kw))
        item["img_link"] = "https:" + response.xpath('//*[@id="detail_bigimg"]/div[1]/img/@src')[0].extract()
        item["link"] = response.url
        item["item_id"] = item["link"].split('/')[-1]
        size_kind = response.xpath('//*[@id="size_table"]/tbody/tr/th/text()').extract()
        item["size_details"] = {}
        for idx in range(len(size_kind)-1):
            sd = response.xpath(f'//*[@id="size_table"]/tbody/tr[{idx+3}]/*/text()').extract()
            item["size_details"][sd[0]] = sd[1:]
            
        sc = response.xpath('//*[@id="size_table"]/thead/tr/th[contains(@class, "item_val")]/text()').extract()
        item["size_category"] = []
        for idx in range(len(sc)):
            if idx % 2 != 0:
                item["size_category"].append(sc[idx].strip())

        yield item
