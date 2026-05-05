# webcrawler/pipelines.py
import sqlite3
import logging
from webcrawler.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

class SQLitePipeline:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
    
    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get('DATABASE_PATH', 'data/crawler.db')
        return cls(db_path)
    
    def open_spider(self, spider):
        db_manager = DatabaseManager(self.db_path)
        db_manager.initialize()
        self.conn = sqlite3.connect(self.db_path)
        logger.info(f"Opened database connection: {self.db_path}")
    
    def close_spider(self, spider):
        if self.conn:
            self.conn.close()
            logger.info("Closed database connection")
    
    def process_item(self, item, spider):
        try:
            self.conn.execute("""
                INSERT INTO crawled_pages (url, title, text_content, metadata_json, status_code, depth)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                item.get('url'),
                item.get('title'),
                item.get('text_content'),
                item.get('metadata_json'),
                item.get('status_code'),
                item.get('depth')
            ))
            self.conn.commit()
            logger.debug(f"Stored item: {item.get('url')}")
        except sqlite3.IntegrityError:
            logger.debug(f"Duplicate URL skipped: {item.get('url')}")
        
        return item
