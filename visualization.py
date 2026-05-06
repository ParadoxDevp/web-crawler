"""Visualization - all analysis and charts."""
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from data_ingestion import DataIngestion
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Visualization:
    """Analyze and visualize crawl data."""
    
    def __init__(self, db_path='sqlite:///data/crawler.db'):
        self.db = DataIngestion(db_path)
        
    def get_stats(self, print_output=True):
        """Get crawl statistics."""
        pages = self.db.get_all()
        df = pd.DataFrame([{
            'url': p.url,
            'status_code': p.status_code,
            'depth': p.depth
        } for p in pages])
        
        stats = {
            'total_pages': len(df),
            'avg_depth': df['depth'].mean() if len(df) > 0 else 0,
            'status_codes': df['status_code'].value_counts().to_dict() if len(df) > 0 else {}
        }
        
        if print_output:
            print("\n=== Crawl Statistics ===")
            print(f"Total Pages: {stats['total_pages']}")
            print(f"Average Depth: {stats['avg_depth']:.2f}")
            print(f"Status Codes: {stats['status_codes']}")
        return stats
        
    def plot_depth_chart(self, output='data/depth_chart.png'):
        """Plot depth distribution."""
        pages = self.db.get_all()
        depths = [p.depth for p in pages]
        
        plt.figure(figsize=(10, 6))
        plt.hist(depths, bins=range(max(depths)+2))
        plt.xlabel('Depth')
        plt.ylabel('Count')
        plt.title('Crawl Depth Distribution')
        plt.savefig(output)
        plt.close()
        print(f"✓ Chart saved: {output}")
        
    def export_csv(self, output='data/results.csv'):
        """Export to CSV."""
        pages = self.db.get_all()
        df = pd.DataFrame([{'url': p.url, 'title': p.title, 'depth': p.depth} for p in pages])
        df.to_csv(output, index=False)
        print(f"✓ Exported {len(df)} rows to {output}")
