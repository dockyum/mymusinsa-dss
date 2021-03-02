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
    size_category = scrapy.Field()
    size_details = scrapy.Field()
