"""Distributed manager - orchestrate workers and queue."""
import redis
import json
from celery import Celery
from core_crawler import CoreCrawler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Celery app
app = Celery('distributed_crawler', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')


class DistributedManager:
    """Manage distributed crawling with Redis queue."""
    
    def __init__(self, redis_host='localhost'):
        self.redis = redis.Redis(host=redis_host, decode_responses=True)
        self.queue_key = 'crawler:queue'
        
    def add_urls(self, urls, priority=0):
        """Add URLs to queue."""
        for url in urls:
            self.redis.zadd(self.queue_key, {json.dumps({'url': url}): -priority})
        print(f"✓ Added {len(urls)} URLs to queue")
        
    def get_next_url(self):
        """Get next URL from queue."""
        result = self.redis.zpopmin(self.queue_key, 1)
        return json.loads(result[0][0])['url'] if result else None
        
    def queue_size(self):
        """Get queue size."""
        return self.redis.zcard(self.queue_key)


@app.task
def crawl_task(url, depth=0):
    """Celery task for crawling."""
    crawler = CoreCrawler()
    return crawler.crawl(url, depth)
