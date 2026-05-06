"""Tests for Redis queue."""
import pytest
from webcrawler.redis_queue import RedisQueue

def test_redis_queue_push_pop():
    queue = RedisQueue(queue_name='test:queue')
    queue.clear()
    
    queue.push('http://example.com', priority=5)
    item = queue.pop()
    
    assert item['url'] == 'http://example.com'
    queue.clear()

def test_redis_queue_priority():
    queue = RedisQueue(queue_name='test:queue')
    queue.clear()
    
    queue.push('http://low.com', priority=1)
    queue.push('http://high.com', priority=10)
    
    item = queue.pop()
    assert item['url'] == 'http://high.com'
    queue.clear()
