# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LibrosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    tags = scrapy.Field()
    sinopsis = scrapy.Field()
    price = scrapy.Field()
    real_price = scrapy.Field()
    n_pages = scrapy.Field()
    editorial = scrapy.Field()
    lang = scrapy.Field()
    encuadernacion = scrapy.Field()
    ISBN = scrapy.Field()
    year = scrapy.Field()
    date = scrapy.Field()

