# webcrawler/spiders/generic_spider.py
import json
import logging
import scrapy
from bs4 import BeautifulSoup
from webcrawler.items import CrawledPage

logger = logging.getLogger(__name__)

class GenericSpider(scrapy.Spider):
    name = 'generic'
    
    def __init__(self, start_urls=None, allowed_domains=None, extraction_rules=None, max_depth=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.allowed_domains = allowed_domains or []
        self.extraction_rules = extraction_rules or {}
        self.max_depth = max_depth
    
    def parse(self, response):
        depth = response.meta.get('depth', 0)
        
        # Extract data using configured rules
        item = CrawledPage()
        item['url'] = response.url
        item['status_code'] = response.status
        item['depth'] = depth
        
        # Extract title
        title_selector = self.extraction_rules.get('title', 'title::text')
        try:
            title = response.css(title_selector).get()
            item['title'] = title.strip() if title else None
        except (AttributeError, Exception) as e:
            logger.warning(f"Failed to extract title from {response.url}: {e}")
            item['title'] = None
        
        # Extract text content
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            for script in soup(["script", "style"]):
                script.decompose()
            text_content = soup.get_text(separator=' ', strip=True)
            item['text_content'] = text_content
        except (AttributeError, TypeError) as e:
            logger.warning(f"Failed to extract text content from {response.url}: {e}")
            item['text_content'] = ''
        
        # Extract metadata
        metadata = {}
        desc_selector = self.extraction_rules.get('description', 'meta[name="description"]::attr(content)')
        try:
            description = response.css(desc_selector).get()
            if description:
                metadata['description'] = description
        except (AttributeError, Exception) as e:
            logger.warning(f"Failed to extract description from {response.url}: {e}")
        item['metadata_json'] = json.dumps(metadata)
        
        yield item
        
        # Follow links if within depth limit
        if depth < self.max_depth:
            links_selector = self.extraction_rules.get('links', 'a::attr(href)')
            try:
                for link in response.css(links_selector).getall():
                    yield response.follow(link, callback=self.parse, meta={'depth': depth + 1})
            except (AttributeError, Exception) as e:
                logger.warning(f"Failed to extract links from {response.url}: {e}")
