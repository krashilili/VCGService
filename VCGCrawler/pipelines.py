# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class SaveItemToMongo(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri= crawler.settings.get('DATABASE').get('default').get('HOST'),
            mongo_db= crawler.settings.get('DATABASE').get('default').get('DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        pass


class SaveDriverItemToMongo(SaveItemToMongo):

    def process_item(self, item, spider):
        coll_n = spider.settings.get('MONGO_DB_COLL')
        drivers_coll = self.db[coll_n]

        unique_driver = {'product_id': item.get('product_id'),
                         'device_driver': item.get('device_driver'),
                         'firmware_version': item.get('firmware_version'),
                         'os_version': item.get('os_version')}

        driver = drivers_coll.find_one(unique_driver)
        if driver:
            # remove the existing driver
            drivers_coll.delete_many(unique_driver)
        spider.logger.info(f"Save the following driver to mongodb. ")
        spider.logger.info(dict(item))
        drivers_coll.insert_one(dict(item))
        return item


class SaveIODataItemToMongo(SaveItemToMongo):

    def process_item(self, item, spider):
        coll_n = spider.settings.get('MONGO_DB_COLL')
        coll = self.db[coll_n]

        product = coll.find_one({'product_id': item.get('product_id')})
        if list(product):
            # remove the existing product
            coll.delete_many({'product_id': item.get('product_id')})
        spider.logger.info(f"Save the following io data to mongodb. ")
        spider.logger.info(dict(item))
        coll.insert_one(dict(item))
        return item
