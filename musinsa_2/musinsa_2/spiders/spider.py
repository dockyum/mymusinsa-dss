
import scrapy
from musinsa_2.items import Musinsa2Item
from selenium import webdriver
from fake_useragent import UserAgent


class Spider(scrapy.Spider):
    name = "Musinsa2"
    allow_domain = ["musinsa.com"]
    start_urls = ["https://search.musinsa.com/category/001003"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 3,
        'DOWNLOAD_DELAY': 6.0,
        'AUTOTHROTTLE_ENABLED': True,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
        }
    }
    
    def parse(self, response):
        links = response.xpath('//*[@id="searchList"]/li/div[contains(@class,"li_inner")]\
/div[2]/p[2]/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_content)
            
    def parse_content(self, response):     
        item = Musinsa2Item()
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("user-agent={}".format(UserAgent().Chrome))
        driver = webdriver.Chrome(options=options)        
        driver.get(response.url)       
        
        try:
            item["most_age"] = driver.find_elements_by_xpath('//*[@id="graph_summary_area"]/strong[1]')[0].text
        except:
            item["most_age"] = 0
        try:
            item["most_sex"] = driver.find_elements_by_xpath('//*[@id="graph_summary_area"]/span[1]')[0].text
        except:
            item["most_sex"] = 0

        option1_ls = driver.find_elements_by_xpath('//*[@id="option1"]/option[not(@value="")]')
        option1 = [option.get_attribute("value") for option in option1_ls]
        driver.find_element_by_xpath('//*[@id="option1"]/option[not(@value="")]').click()
        option2_ls = driver.find_elements_by_xpath('//*[@id="option2"]/option[not(@value="")]')
        option2 = [option.get_attribute("value") for option in option2_ls]

        for_size = ['90', '95', 'S', 'M', 'L', 'LARGE', '1', 'M_쭈리']
        if any(x in for_size for x in option1):
            item["sizes"] = option1
            item["colors"] = option2
        else:
            item["sizes"] = option2
            item["colors"] = option1

        driver.quit()
        
        item["item_id"] = response.url.split('/')[-1]
        
        yield item
