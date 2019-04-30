from scrapy import cmdline
# cmdline.execute("scrapy crawl vendor_spider".split())
# cmdline.execute("scrapy crawl id_date_spider".split())
cmdline.execute("scrapy crawl vcg_driver_spider -a vid=14e4 -a did=163a -a svid=105b -a ssid=0cff -s LOG_FILE=vcg_driver_crawler.log".split())
# cmdline.execute("scrapy crawl vcg_io_data_spider -s LOG_FILE=io_data_crawler.log".split())