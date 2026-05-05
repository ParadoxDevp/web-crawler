# webcrawler/items.py
import scrapy

class CrawledPage(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text_content = scrapy.Field()
    metadata_json = scrapy.Field()
    status_code = scrapy.Field()
    depth = scrapy.Field()
