import scrapy
from scrapy import Request
import json
from ..items import MyntrascraperItem
import re


class MyntraspiderSpider(scrapy.Spider):
    name = 'myntraspider'
    # allowed_domains = ['myntra.com']
    # start_urls = ['http://myntra.com/']
    count = 1
    headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }


    def start_requests(self):
        start_url = "https://www.myntra.com/dresses"
        yield scrapy.Request(start_url,headers=self.headers,callback=self.product_page_list, dont_filter=True)

    def product_page_list(self, response):
        data = response.xpath('//script[contains(.,"searchData")]/text()').extract_first()
        replaced_data = data.replace("window.__myx = ", "")
        json_data = json.loads(replaced_data)

        
        product_details_block = json_data['searchData']['results']['products']
        for product_block in product_details_block:
            product_url = product_block['landingPageUrl']
            product_url = "https://www.myntra.com/" + product_url
            # print(product_url)
         
            product_id = product_block['productId']

            product_name = product_block['productName']

            rating = product_block['rating']
            product_rating = round(rating, 1)

            product_rating_count = product_block['ratingCount']

            product_discount_value = product_block['discount']
            if product_discount_value != 0:
               product_discount = "₹" + str(product_discount_value)
            else:
                product_discount = str(product_discount_value)

            product_brand = product_block['brand']

            product_image = product_block['searchImage']

            discount_label = product_block['discountDisplayLabel']
            product_discount_label = re.search(r'(\d+%)', discount_label)
            if product_discount_label:
                product_discount_label = product_discount_label.group()
            else:
                product_discount_label = None

            product_mrp_value = product_block['mrp']
            if product_mrp_value != 0:
                product_mrp = "₹" + str(product_mrp_value)
            else:
                product_mrp = str(product_mrp_value)

            product_price_value = product_block['price']
            if product_price_value != 0:
                product_price = "₹" + str(product_price_value)
            else:
                product_price = str(product_price_value)

            product_season = product_block['season']
            #product_availability = product_block.get('available', None)

            product = MyntrascraperItem()
            product["p_url"] = product_url
            product["p_id"] = product_id
            product["p_name"] = product_name
            product["p_rating"] = product_rating
            product["p_rating_count"] = product_rating_count
            product["p_discount"] = product_discount
            product["p_brand"] = product_brand
            product["p_image"] = product_image
            product["p_discount_label"] = product_discount_label
            product["p_mrp"] = product_mrp
            product["p_price"] = product_price
            product["p_season"] = product_season
            # product["p_availability"] = product_availability 

            yield product

    def next_page_list(self, response):
        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page:
            next_page_link = next_page
            MyntraspiderSpider.count += 1
            if MyntraspiderSpider.count < 50:
                yield Request(next_page_link, headers=self.headers, callback=self.product_page_list, dont_filter=True)










        
