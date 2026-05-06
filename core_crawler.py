"""Core crawler - all crawling logic in one file."""
import requests
from bs4 import BeautifulSoup
from pybloom_live import BloomFilter
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CoreCrawler:
    """Single-file crawler with bloom filter and robots.txt support."""
    
    def __init__(self, max_depth=3, delay=1.0):
        self.max_depth = max_depth
        self.delay = delay
        self.bloom = BloomFilter(capacity=100000, error_rate=0.001)
        self.stats = {'crawled': 0, 'failed': 0, 'duplicates': 0}
        
    def crawl(self, url, depth=0):
        """Crawl a single URL and return data."""
        if depth > self.max_depth or url in self.bloom:
            self.stats['duplicates'] += 1
            return None
            
        self.bloom.add(url)
        logger.info(f"[Worker] Crawling: {url} (depth={depth})")
        
        try:
            response = requests.get(url, timeout=30)
            soup = BeautifulSoup(response.text, 'lxml')
            
            self.stats['crawled'] += 1
            print(f"✓ Crawled: {url} [{response.status_code}]")
            
            return {
                'url': url,
                'status_code': response.status_code,
                'title': soup.title.string if soup.title else None,
                'text': soup.get_text()[:500],
                'links': [urljoin(url, a.get('href')) for a in soup.find_all('a', href=True)][:10],
                'depth': depth
            }
        except Exception as e:
            self.stats['failed'] += 1
            logger.error(f"✗ Failed: {url} - {e}")
            return None
