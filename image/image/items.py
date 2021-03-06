import scrapy


class ImageItem(scrapy.Item):
    img_link = scrapy.Field()
    item_id = scrapy.Field()
