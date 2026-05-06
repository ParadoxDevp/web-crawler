"""Distributed crawler coordinator using Celery and Redis."""
from webcrawler.celery_app import crawl_url
from webcrawler.redis_queue import RedisQueue
from webcrawler.bloom_filter import URLBloomFilter
from webcrawler.models import get_engine, get_session, init_db, CrawledPage
import logging

logger = logging.getLogger(__name__)


class DistributedCrawler:
    """Coordinate distributed crawling across multiple workers."""
    
    def __init__(self, redis_host='localhost', db_path='sqlite:///data/crawler.db'):
        self.queue = RedisQueue(host=redis_host)
        self.bloom = URLBloomFilter()
        self.engine = get_engine(db_path)
        init_db(self.engine)
        
    def add_seed_urls(self, urls, priority=10):
        """Add seed URLs to queue."""
        for url in urls:
            if not self.bloom.contains(url):
                self.queue.push(url, priority)
                self.bloom.add(url)
                
    def start_crawl(self, max_depth=3):
        """Start distributed crawl."""
        while self.queue.size() > 0:
            item = self.queue.pop()
            if item:
                url = item['url']
                depth = item.get('metadata', {}).get('depth', 0)
                crawl_url.delay(url, depth, max_depth)
