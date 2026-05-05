import sqlite3
import logging
import os

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def initialize(self):
        """Create database schema with WAL mode for concurrent access."""
        try:
            db_dir = os.path.dirname(self.db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)
            
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA journal_mode=WAL")
                
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS crawled_pages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        url TEXT UNIQUE NOT NULL,
                        title TEXT,
                        text_content TEXT,
                        metadata_json TEXT,
                        crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status_code INTEGER,
                        depth INTEGER
                    )
                """)
                
                conn.execute("CREATE INDEX IF NOT EXISTS idx_url ON crawled_pages(url)")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_crawled_at ON crawled_pages(crawled_at)")
                
                conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except (sqlite3.Error, OSError, PermissionError) as e:
            logger.error(f"Failed to initialize database at {self.db_path}: {e}")
            raise
