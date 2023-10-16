# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyntrascraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    p_url = scrapy.Field()
    p_id = scrapy.Field()
    p_name = scrapy.Field()
    p_rating = scrapy.Field()
    p_rating_count = scrapy.Field()
    p_discount = scrapy.Field()
    p_brand = scrapy.Field()
    p_image = scrapy.Field()
    p_discount_label = scrapy.Field()
    p_mrp = scrapy.Field()
    p_price = scrapy.Field()
    p_season = scrapy.Field()
    #p_availability = scrapy.Field()
