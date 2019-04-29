import scrapy, re, json, pymongo
from ..items import VCGDriverItem
from ..settings import DATABASE, DRIVER_URL_PREX

default_db = DATABASE.get('default')
db = pymongo.MongoClient(default_db.get('HOST'))[default_db.get('DB')]
io_data_coll = db[default_db.get('IOData_COLL')]


class VCGDriverSpider(scrapy.Spider):
    name = "vcg_driver_spider"

    custom_settings = {
        'MONGO_DB_COLL': 'drivers',
    }

    BASIC_URL = DRIVER_URL_PREX+"&productid={product_id}&VID={vid}"

    def start_requests(self):
        self.vid, self.did, self.svid, self.ssid = "14e4", "163a", "105b", "0cff"

        # get the product id from `io_data` collection
        self.product_id = io_data_coll.find_one({'vid': self.vid,
                                                 'did': self.did,
                                                 'svid': self.svid,
                                                 'ssid': self.ssid}).get('product_id')

        if self.product_id:
            start_url = self.BASIC_URL.format(product_id=self.product_id,
                                              vid=self.vid)
            yield scrapy.Request(start_url)

    def parse(self, response):

        text_str = response.text

        # find the matched details
        regex_details = r"""var details =\[(.*)]"""
        driver_str =re.compile(regex_details, re.M).findall(text_str)[0]

        # find all drivers in the details
        regex_drivers = r"""{.+?}"""
        drivers = re.compile(regex_drivers, re.M).findall(driver_str)

        # save the driver to driver_item
        for driver in drivers:
            driver_dict = json.loads(driver)

            driver_item = VCGDriverItem()
            # ids
            driver_item['product_id'] = self.product_id
            driver_item['vid'] = self.vid
            driver_item['did'] = self.did
            driver_item['svid'] = self.svid
            driver_item['ssid'] = self.ssid
            # driver info
            driver_item['driver_name'] = driver_dict.get('DriverName')
            driver_item['driver_version'] = driver_dict.get('Version')
            url = driver_dict.get('Driver_Url')
            driver_item['driver_url'] = url.replace('amp;','')
            driver_item['os_version'] = driver_dict.get('ReleaseVersion')
            driver_item['inbox_async'] = driver_dict.get('inbox_async')
            driver_item['device_driver'] = driver_dict.get('DeviceDrivers')
            driver_item['firmware_version'] = driver_dict.get('FirmwareVersion')
            driver_item['vmware_support_date'] = driver_dict.get('VMwareSupportDate')
            driver_item['vmklinux_or_native'] = driver_dict.get('VmklinuxOrNativeDriver')

            yield driver_item
