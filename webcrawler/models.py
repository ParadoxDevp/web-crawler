"""SQLAlchemy ORM models for crawler data."""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class CrawledPage(Base):
    __tablename__ = 'crawled_pages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False, index=True)
    title = Column(String)
    text_content = Column(Text)
    metadata_json = Column(Text)
    crawled_at = Column(DateTime, default=datetime.utcnow, index=True)
    status_code = Column(Integer)
    depth = Column(Integer)


def get_engine(db_path='sqlite:///data/crawler.db'):
    return create_engine(db_path, echo=False)


def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def init_db(engine):
    Base.metadata.create_all(engine)
