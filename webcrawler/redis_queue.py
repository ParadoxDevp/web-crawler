"""Redis-based distributed URL queue with priority support."""
import redis
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class RedisQueue:
    """Distributed priority queue using Redis."""
    
    def __init__(self, host='localhost', port=6379, db=0, queue_name='crawler:queue'):
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.queue_name = queue_name
        
    def push(self, url: str, priority: int = 0, metadata: Optional[Dict[str, Any]] = None):
        """Add URL to queue with priority (higher = processed first)."""
        item = {'url': url, 'metadata': metadata or {}}
        self.redis_client.zadd(self.queue_name, {json.dumps(item): -priority})
        logger.debug(f"Added to queue: {url} (priority: {priority})")
        
    def pop(self) -> Optional[Dict[str, Any]]:
        """Get highest priority URL from queue."""
        result = self.redis_client.zpopmin(self.queue_name, 1)
        if result:
            item_json, _ = result[0]
            return json.loads(item_json)
        return None
        
    def size(self) -> int:
        """Get queue size."""
        return self.redis_client.zcard(self.queue_name)
        
    def clear(self):
        """Clear all items from queue."""
        self.redis_client.delete(self.queue_name)
