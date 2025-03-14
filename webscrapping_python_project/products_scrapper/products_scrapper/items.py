# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    product_title = scrapy.Field()
    product_url = scrapy.Field()
    product_price = scrapy.Field()
    product_description = scrapy.Field()
    shop = scrapy.Field()
    scraping_date = scrapy.Field()
    ean = scrapy.Field()
    quantity_available = scrapy.Field()
    image_url = scrapy.Field()
