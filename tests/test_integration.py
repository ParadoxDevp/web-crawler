# tests/test_integration.py
import pytest
import os
import tempfile
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from webcrawler.spiders.generic_spider import GenericSpider
from webcrawler.db_manager import DatabaseManager

@pytest.mark.skip(reason="Integration test requires network access - run manually")
def test_full_crawl_workflow():
    """Integration test: crawl example.com and verify data is stored."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test.db")
        
        settings = {
            'CONCURRENT_REQUESTS': 1,
            'DOWNLOAD_DELAY': 1.0,
            'DATABASE_PATH': db_path,
            'LOG_LEVEL': 'ERROR',
            'ROBOTSTXT_OBEY': True,
            'ITEM_PIPELINES': {'webcrawler.pipelines.SQLitePipeline': 300},
        }
        
        runner = CrawlerRunner(settings)
        
        @defer.inlineCallbacks
        def crawl():
            yield runner.crawl(
                GenericSpider,
                start_urls=["http://example.com"],
                extraction_rules={"title": "h1::text"},
                max_depth=1
            )
            reactor.stop()
        
        crawl()
        reactor.run()
        
        # Verify data was stored
        db = DatabaseManager(db_path)
        import sqlite3
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute("SELECT * FROM crawled_pages")
            pages = cursor.fetchall()
        
        assert len(pages) > 0
        assert any("example.com" in page[1] for page in pages)
