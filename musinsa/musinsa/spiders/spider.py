
import scrapy
from musinsa.items import MusinsaItem


class Spider(scrapy.Spider):
    name = "Musinsa"
    allow_domain = ["musinsa.com"]
    start_urls = ["https://search.musinsa.com/category/001003"]

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
        try: # 세일가 있는 상품
            item["o_price"] = response.xpath('//*[@id="goods_price"]/del/text()')[0].extract().strip()
        except: # 판매가만 있는 상품
            item["o_price"] = response.xpath('//*[@id="goods_price"]/text()')[0].extract().strip()
        try:
            item["s_price"] = response.xpath('//*[@id="sale_price"]/text()')[0].extract().strip()
        except:
            item["s_price"] = item["o_price"]
        try:
            item["kw"] = response.xpath('//*[@id="product_order_info"]/div[1]/ul/li[7]/p/a/text()').extract()
        except:
            item["kw"] = ''
        item["img_link"] = "https:" + response.xpath('//*[@id="detail_bigimg"]/div[1]/img/@src')[0].extract()
        item["link"] = response.url
        yield item       
