# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    core = scrapy.Field()
    ram = scrapy.Field()
    screen = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
