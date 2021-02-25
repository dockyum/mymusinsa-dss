import scrapy


class MusinsaItem(scrapy.Item):
    title = scrapy.Field()
    brand = scrapy.Field()
    o_price = scrapy.Field()
    s_price = scrapy.Field()
    kw = scrapy.Field()
    img_link = scrapy.Field()
    link = scrapy.Field()
    item_id = scrapy.Field()
    most_age = scrapy.Field()
    most_sex = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
    size_details = scrapy.Field()
