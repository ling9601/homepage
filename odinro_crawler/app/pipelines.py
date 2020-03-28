# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# from pymongo import MongoClient
from crawler.models import StoreItem_dj, BaseItem_dj
from app.items import StoreItem, BaseItem

class DjangoPipeLine(object):
    def process_item(self, item, spider):
        if isinstance(item, StoreItem):
            StoreItem_dj(**item, scrapy_item=spider.scrapy_item).save(force_insert=True)
        elif isinstance(item, BaseItem):
            BaseItem_dj(**item).save(force_insert=True)
        return item

## use for StoreItem
# class MongoPipeline(object):

#     collection_name = 'StoreItem'

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE')
#         )

#     def open_spider(self, spider):
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.col = self.db[self.collection_name]
#         # clean collections
#         self.col.remove()
#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.col.insert_one(dict(item))
#         return item

# class MongoPipeline(object):

#     collection_name = 'BaseItem'

#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db

#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE')
#         )

#     def open_spider(self, spider):
#         self.client = MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#         self.col = self.db[self.collection_name]
#         self.col.create_index("id", unique=True)
#         # clean collections
#         self.col.remove()
#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.col.insert_one(dict(item))
#         return item