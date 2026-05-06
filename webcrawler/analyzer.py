"""Data analysis module using pandas."""
import pandas as pd
import sqlite3
import logging

logger = logging.getLogger(__name__)


class CrawlAnalyzer:
    """Analyze crawled data using pandas."""
    
    def __init__(self, db_path='data/crawler.db'):
        self.db_path = db_path
        
    def load_data(self) -> pd.DataFrame:
        """Load crawled data into DataFrame."""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM crawled_pages", conn)
        conn.close()
        return df
        
    def get_stats(self) -> dict:
        """Get crawl statistics."""
        df = self.load_data()
        return {
            'total_pages': len(df),
            'unique_domains': df['url'].apply(lambda x: x.split('/')[2] if '://' in x else '').nunique(),
            'avg_depth': df['depth'].mean(),
            'status_codes': df['status_code'].value_counts().to_dict()
        }
        
    def export_csv(self, output_path='data/crawl_results.csv'):
        """Export data to CSV."""
        df = self.load_data()
        df.to_csv(output_path, index=False)
        logger.info(f"Exported {len(df)} records to {output_path}")
