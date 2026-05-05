# tests/test_spider.py
import json
from scrapy.http import HtmlResponse, Request
from webcrawler.spiders.generic_spider import GenericSpider

def test_spider_parses_page():
    spider = GenericSpider(
        start_urls=["http://example.com"],
        extraction_rules={"title": "h1::text"}
    )
    
    html = "<html><body><h1>Test Title</h1><a href='/page2'>Link</a></body></html>"
    request = Request(url="http://example.com")
    response = HtmlResponse(url="http://example.com", body=html.encode('utf-8'), request=request)
    
    results = list(spider.parse(response))
    
    assert len(results) > 0
    item = results[0]
    assert item['url'] == "http://example.com"
    assert item['title'] == "Test Title"
