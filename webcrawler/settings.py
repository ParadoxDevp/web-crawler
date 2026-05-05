# Scrapy settings for webcrawler project
BOT_NAME = 'webcrawler'

SPIDER_MODULES = ['webcrawler.spiders']
NEWSPIDER_MODULE = 'webcrawler.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 3

DOWNLOAD_DELAY = 1.0

DOWNLOAD_TIMEOUT = 30

RETRY_TIMES = 3

ITEM_PIPELINES = {
    'webcrawler.pipelines.SQLitePipeline': 300,
}

DATABASE_PATH = 'data/crawler.db'

LOG_LEVEL = 'INFO'
LOG_FILE = 'data/crawler.log'

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
