# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    page = scrapy.Field()
    url = scrapy.Field()
    img_src = scrapy.Field()
    pass
