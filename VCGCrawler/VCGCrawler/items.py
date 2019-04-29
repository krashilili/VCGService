# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VcgcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class IODataItem(scrapy.Item):
    product_id = scrapy.Field()
    vid = scrapy.Field()
    did = scrapy.Field()
    svid = scrapy.Field()
    ssid = scrapy.Field()


class VCGDriverItem(IODataItem):
    driver_name = scrapy.Field()
    driver_version = scrapy.Field()
    driver_url = scrapy.Field()
    os_version = scrapy.Field()
    inbox_async = scrapy.Field()
    device_driver = scrapy.Field()
    firmware_version = scrapy.Field()
    vmklinux_or_native = scrapy.Field()
    vmware_support_date = scrapy.Field()