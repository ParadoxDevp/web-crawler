"""Visualization module using matplotlib and networkx."""
import matplotlib.pyplot as plt
import networkx as nx
import sqlite3
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class CrawlVisualizer:
    """Visualize crawl data and network graphs."""
    
    def __init__(self, db_path='data/crawler.db'):
        self.db_path = db_path
        
    def plot_depth_distribution(self, output='data/depth_dist.png'):
        """Plot distribution of pages by depth."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT depth, COUNT(*) FROM crawled_pages GROUP BY depth")
        data = cursor.fetchall()
        conn.close()
        
        depths, counts = zip(*data) if data else ([], [])
        plt.figure(figsize=(10, 6))
        plt.bar(depths, counts)
        plt.xlabel('Depth')
        plt.ylabel('Page Count')
        plt.title('Pages by Crawl Depth')
        plt.savefig(output)
        plt.close()
        logger.info(f"Saved depth distribution to {output}")
