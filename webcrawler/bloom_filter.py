"""Bloom filter for efficient duplicate URL detection."""
from pybloom_live import BloomFilter
import logging

logger = logging.getLogger(__name__)


class URLBloomFilter:
    """Memory-efficient duplicate detection using bloom filter."""
    
    def __init__(self, capacity=1000000, error_rate=0.001):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        
    def add(self, url: str):
        """Add URL to bloom filter."""
        self.bloom.add(url)
        
    def contains(self, url: str) -> bool:
        """Check if URL might be duplicate (false positives possible)."""
        return url in self.bloom
        
    def __len__(self):
        return self.bloom.count
