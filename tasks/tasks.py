from celery.app import shared_task
from celery.app.base import Celery
from celery.contrib import rdb
from scrapy.crawler import Crawler
from billiard.context import Process
from scrapy.utils.project import get_project_settings
from VCGCrawler.spiders.VCGDriverSpider import VCGDriverSpider

from celery.utils.log import get_task_logger

app = Celery('tasks',
             broker='amqp://guest:guest@localhost:5672',
             backend='db+sqlite:///results.sqlite')
app.config_from_object('celeryconfig')

logger = get_task_logger(__name__)


class UrlCrawlerScript(Process):
        def __init__(self, spider):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(settings)
            self.crawler.configure()
            # self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
            self.spider = spider

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            # reactor.run()


def run_spider(vid, did, svid, ssid):
    # vid = args.get('vid')
    # did = args.get('did')
    # svid = args.get('svid')
    # ssid = args.get('ssid')
    logger.info("Running spider")
    logger.info(vid)
    # rdb.set_trace()
    spider = VCGDriverSpider(vid=vid, did=did,svid=svid, ssid=ssid)
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()
    return "Done"

#
# @app.task
# def crawl(**kwargs):
#     print("Args: ")
#     print(kwargs)
#     return run_spider(**kwargs)

@app.task
def add(a,b):
    x= a+b
    return x