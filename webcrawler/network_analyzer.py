"""Network analysis module using scapy."""
from scapy.all import sniff, IP, TCP
import logging

logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """Analyze network traffic during crawling."""
    
    def __init__(self):
        self.packets = []
        
    def capture_packets(self, count=100, filter_str="tcp port 80 or tcp port 443"):
        """Capture HTTP/HTTPS packets."""
        logger.info(f"Capturing {count} packets...")
        self.packets = sniff(count=count, filter=filter_str)
        return len(self.packets)
        
    def get_stats(self) -> dict:
        """Get packet statistics."""
        if not self.packets:
            return {}
        return {
            'total_packets': len(self.packets),
            'protocols': {p[IP].proto for p in self.packets if IP in p}
        }
