"""Data ingestion - database operations and storage."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base = declarative_base()


class CrawledPage(Base):
    __tablename__ = 'crawled_pages'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String)
    text_content = Column(Text)
    status_code = Column(Integer)
    depth = Column(Integer)
    crawled_at = Column(DateTime, default=datetime.utcnow)


class DataIngestion:
    """Handle all database operations."""
    
    def __init__(self, db_path='sqlite:///data/crawler.db'):
        self.engine = create_engine(db_path)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def save(self, data):
        """Save crawled data."""
        try:
            existing = self.session.query(CrawledPage).filter_by(url=data['url']).first()
            if existing:
                print(f"⊘ Duplicate skipped: {data['url']}")
                return
            
            page = CrawledPage(
                url=data['url'],
                title=data.get('title'),
                text_content=data.get('text'),
                status_code=data.get('status_code'),
                depth=data.get('depth')
            )
            self.session.add(page)
            self.session.commit()
            print(f"✓ Saved: {data['url']}")
        except Exception as e:
            self.session.rollback()
            logger.debug(f"Save error: {e}")
            
    def get_all(self):
        """Get all crawled pages."""
        return self.session.query(CrawledPage).all()
