import scrapy, re, json
from ..items import IODataItem
from ..settings import DATABASE, IOData_URL


class IODataSpider(scrapy.Spider):
    name = "vcg_io_data_spider"
    IO_DATA_URL = IOData_URL
    custom_settings = {
        'MONGO_DB_COLL': DATABASE.get('default').get('IOData_COLL'),
        'ITEM_PIPELINES': {
            'VCGCrawler.pipelines.SaveIODataItemToMongo': 100,
        }
    }

    def start_requests(self):
        start_url = self.IO_DATA_URL
        yield scrapy.Request(start_url)

    def parse(self, response):
        resp_text = response.text

        # match all devices with partner id of 23 (Dell)
        regex_dell = r"""^\s*\[\"[0-9]+\",\s*\"23\".*]"""
        dell_devices = [json.loads(s) for s in re.compile(regex_dell, re.M).findall(resp_text)]
        for device in dell_devices:
            item = IODataItem()
            item['product_id'] = device[0]
            item['vid'] = device[4]
            item['did'] = device[5]
            item['svid'] = device[6]
            item['ssid'] = device[7]
            yield item
