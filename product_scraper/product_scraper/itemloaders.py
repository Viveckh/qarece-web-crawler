from scrapy.loader import ItemLoader
from product_scraper.items import Product
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Join
from scrapy.selector import Selector
import re
import json

clean_text = Compose(MapCompose(lambda v: v.strip()), Join())   
to_int = Compose(TakeFirst(), int)

def extract_with_css(response, query):
    return response.css(query).get(default='').strip()

class ProductItemLoader(ItemLoader):

    #default_output_processor = clean_text

    def parse_macys(self, product_url, html_dump):
        loader = ProductItemLoader(item=Product(), selector=html_dump)

        hxs = Selector(html_dump)
        json_dump = hxs.select('//script[contains(@data-bootstrap, "feature/product")]/text()').extract()[0]
        data = json.loads(json_dump)

        loader.add_value('product_url', product_url)
        loader.add_value('product_id', data['product']['id'])
        loader.add_value('name', data['product']['detail']['name'])
        loader.add_value('brand', data['product']['detail']['brand']['name'])
        loader.add_value('description', data['product']['detail']['description'])
        loader.add_value('sale_price', data['product']['pricing']['price']['tieredPrice'][0]['values'][0]['value'])
        '''
        loader.add_css('name', 'div[data-auto="product-title"] .product-brand-title a::text')
        loader.add_css('brand', 'div[data-auto="product-title"] .product-name::text')
        loader.add_value('description', 'div[data-section="product-details"] div[data-el="product-details"]')
        loader.add_css('picture_url', )
        loader.add_css('marked_price', )
        loader.add_css('sale_price', 'div[data-el="price-details"] div[data-auto="main-price"]')
        '''
        return loader.load_item()

    def parse_kylie_cosmetics(self, product_url, html_dump):
        loader = ProductItemLoader(item=Product(), selector=html_dump)

        return loader.load_item()
    