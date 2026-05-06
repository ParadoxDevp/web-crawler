"""Tests for analyzer."""
import pytest
import sqlite3
from webcrawler.analyzer import CrawlAnalyzer

def test_analyzer_get_stats(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("""CREATE TABLE crawled_pages (
        id INTEGER PRIMARY KEY, url TEXT, title TEXT, 
        text_content TEXT, metadata_json TEXT, 
        crawled_at TIMESTAMP, status_code INTEGER, depth INTEGER
    )""")
    conn.execute("INSERT INTO crawled_pages (url, status_code, depth) VALUES (?, ?, ?)",
                 ('http://example.com', 200, 1))
    conn.commit()
    conn.close()
    
    analyzer = CrawlAnalyzer(str(db_path))
    stats = analyzer.get_stats()
    
    assert stats['total_pages'] == 1
