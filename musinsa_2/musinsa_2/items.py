import scrapy


class Musinsa2Item(scrapy.Item):
    item_id = scrapy.Field()
    most_age = scrapy.Field()
    most_sex = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
