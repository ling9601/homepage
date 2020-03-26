# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Identity
from scrapy.loader import ItemLoader
from scrapy import Field
import re

def filter_non_digit(string):
    return re.sub("[^0-9]", "", string)

class BaseItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    id_out = Compose(TakeFirst(),int)

class BaseItem(scrapy.Item):

    id = Field()
    image_link = Field()
    name = Field()
    genre = Field()
    equipment_location = Field()
    buy_price = Field()
    sell_price = Field()
    weight = Field()
    atk = Field()
    matk = Field()
    defense = Field()
    attack_distance = Field()
    hole_num = Field()
    refinable = Field()

    def __repr__(self):
        return repr({'id': self['id'],"name": self['name']})

class StoreItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    item_id_out = Compose(TakeFirst(), int)
    price_out = Compose(TakeFirst(), filter_non_digit, int)
    level_out = Compose(TakeFirst(), int)
    num_out = Compose(TakeFirst(), int)
    store_id_out = Compose(TakeFirst(), int)
    hole_num_out = Compose(TakeFirst(), filter_non_digit, int)

    time_in = Identity()
    time_out = TakeFirst()

class StoreItem(scrapy.Item):
    
    store_name = Field()
    store_id = Field()
    position = Field()
    name = Field()
    item_id = Field()
    hole_num = Field()
    hole_1 = Field()
    hole_2 = Field()
    hole_3 = Field()
    hole_4 = Field()
    level = Field()
    price = Field()
    num = Field()
    time = Field()

    def __repr__(self):
        return repr({'id':self['item_id'], 'name':self['name']})

