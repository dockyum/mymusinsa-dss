
import scrapy
from size.items import SizeItem
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Size"
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
        item = SizeItem()
        item["item_id"] = response.url.split('/')[-1]

        # 사이즈 카테고리
        sc = response.xpath('//*[@id="size_table"]/thead/tr/th[contains(@class, "item_val")]/text()').extract()
        size_category = []
        for idx in range(len(sc)):
            if idx % 2 != 0:
                size_category.append(sc[idx].strip())

        # 사이즈 카테고리 하나씩 분리
        sc_ls = ["_0", "_1", "_2", "_3", "_4", "_5"]
        for x in range(len(sc_ls)):
            try:
                item[sc_ls[x]] = size_category[x]
            except:
                item[sc_ls[x]] = 0



        # 사이즈 종류
        size_kind = response.xpath('//*[@id="size_table"]/tbody/tr/th/text()').extract()[1:]

        # 사이즈 종류 하나씩 분리
        sk_ls = ["A", "B", "C", "D", "E", "F", "G"]
        for y in range(len(sk_ls)):
            try:
                item[sk_ls[y]] = size_kind[y]
            except:
                item[sk_ls[y]] = 0
                

        # 사이즈 수치
        size_details = {}

        for idx in range(len(size_kind)):
            sd = response.xpath(f'//*[@id="size_table"]/tbody/tr[{idx+3}]/*/text()').extract()
            size_details[sd[0]] = sd[1:]

        # 사이즈 수치별 변수
        for aa, bb in enumerate(sk_ls):
            for cc, dd in enumerate(sc_ls):
                try:
                    item[bb+dd] = size_details[size_kind[aa]][cc]
                except:
                    item[bb+dd] = 0
                    
        yield item
