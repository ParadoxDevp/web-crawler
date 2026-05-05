# tests/test_pipeline.py
import sqlite3
import json
import pytest
from webcrawler.pipelines import SQLitePipeline
from webcrawler.items import CrawledPage

def test_pipeline_stores_item(tmp_path):
    db_path = tmp_path / "test.db"
    pipeline = SQLitePipeline(str(db_path))
    pipeline.open_spider(None)
    
    item = CrawledPage(
        url="http://example.com",
        title="Test Page",
        text_content="Test content",
        metadata_json=json.dumps({"key": "value"}),
        status_code=200,
        depth=1
    )
    
    pipeline.process_item(item, None)
    pipeline.close_spider(None)
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT url, title FROM crawled_pages WHERE url=?", ("http://example.com",))
    row = cursor.fetchone()
    conn.close()
    
    assert row is not None
    assert row[0] == "http://example.com"
    assert row[1] == "Test Page"
