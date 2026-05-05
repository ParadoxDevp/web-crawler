# Distributed Web Crawler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Scrapy-based web crawler with 2-5 concurrent workers, SQLite storage, robots.txt compliance, and configurable extraction rules.

**Architecture:** Scrapy framework with custom spider, SQLite pipeline, YAML configuration, and CLI interface. Uses Scrapy's built-in duplicate filtering, robots.txt middleware, and retry logic.

**Tech Stack:** Python 3.8+, Scrapy 2.11+, SQLite3, BeautifulSoup4, PyYAML

---

## Implementation Notes

- All tests use TDD approach: write test, verify failure, implement, verify pass
- Keep extraction rules simple and configurable via CSS selectors
- SQLite WAL mode enables concurrent access for multiple workers
- Scrapy handles robots.txt, duplicate filtering, and retries automatically
- Each task produces working, testable code before moving to next task
- Commit frequently after each passing test

## Success Criteria

✓ Successfully crawl 2-5 websites concurrently
✓ Respect robots.txt and rate limits
✓ Extract structured data, text, and metadata as configured
✓ Store results in SQLite without data loss
✓ Handle errors gracefully with retries
✓ Provide clear logging and statistics
✓ Support config file and CLI overrides
✓ Complete graceful shutdown on interrupt


**Files:**
- Verify: All components working together

- [ ] **Step 1: Run full crawl with default config**

Run: `python crawler.py --urls "http://example.com" --depth 1`
Expected: Crawler starts, fetches pages, stores to database, completes without errors

- [ ] **Step 2: Verify database contents**

Run: `sqlite3 data/crawler.db "SELECT COUNT(*) FROM crawled_pages;"`
Expected: Shows count > 0

- [ ] **Step 3: Check stored data**

Run: `sqlite3 data/crawler.db "SELECT url, title, status_code FROM crawled_pages LIMIT 5;"`
Expected: Shows crawled URLs with titles and status codes

- [ ] **Step 4: Verify logs**

Run: `tail -20 data/crawler.log`
Expected: Shows crawl activity, no critical errors

- [ ] **Step 5: Test robots.txt compliance**

Run: `python crawler.py --urls "http://www.google.com/search" --depth 0`
Expected: Respects robots.txt, may skip disallowed paths

- [ ] **Step 6: Final commit**

```bash
git add -A
git commit -m "chore: final verification and cleanup"
```

---


**Files:**
- Create: `README.md`

- [ ] **Step 1: Create README.md**

```markdown
# Distributed Web Crawler

A Scrapy-based web crawler with concurrent workers, SQLite storage, and configurable extraction rules.

## Features

- 2-5 concurrent workers
- robots.txt compliance
- Duplicate URL detection
- Configurable data extraction (structured data, text, metadata)
- SQLite storage with WAL mode
- Simple retry logic (3 attempts)
- YAML configuration with CLI overrides

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage with default config:
```bash
python crawler.py
```

### Custom configuration:
```bash
python crawler.py --config custom.yaml
```

### Override settings:
```bash
python crawler.py --workers 5 --delay 2 --depth 5
```

### Specify seed URLs directly:
```bash
python crawler.py --urls "http://example.com" "http://test.com"
```

## Configuration

Edit `config.yaml` to customize:
- `seed_urls`: Starting URLs
- `allowed_domains`: Domain restrictions (optional)
- `max_depth`: Crawl depth limit
- `concurrent_requests`: Number of concurrent workers (2-5)
- `download_delay`: Delay between requests (seconds)
- `extraction_rules`: CSS selectors for data extraction

## Database

Crawled data is stored in `data/crawler.db`. Query with:

```bash
sqlite3 data/crawler.db "SELECT url, title FROM crawled_pages LIMIT 10;"
```

## Testing

```bash
pytest tests/ -v
```

## Logs

View logs at `data/crawler.log`
```

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "docs: add README with usage instructions"
```

---


**Files:**
- Create: `tests/test_integration.py`

- [ ] **Step 1: Write integration test**

```python
# tests/test_integration.py
import os
import sqlite3
import pytest
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from webcrawler.spiders.generic_spider import GenericSpider

@pytest.mark.skip(reason="Requires network access - run manually")
def test_full_crawl_workflow(tmp_path):
    """Integration test - crawls example.com and stores to database."""
    db_path = tmp_path / "test.db"
    
    settings = get_project_settings()
    settings.set('DATABASE_PATH', str(db_path))
    settings.set('LOG_LEVEL', 'DEBUG')
    
    runner = CrawlerRunner(settings)
    
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(
            GenericSpider,
            start_urls=["http://example.com"],
            allowed_domains=["example.com"],
            extraction_rules={"title": "h1::text"},
            max_depth=1
        )
        reactor.stop()
    
    crawl()
    reactor.run()
    
    # Verify data was stored
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM crawled_pages")
    count = cursor.fetchone()[0]
    conn.close()
    
    assert count > 0
```

- [ ] **Step 2: Run unit tests**

Run: `pytest tests/ -v -k "not integration"`
Expected: All unit tests pass

- [ ] **Step 3: Commit**

```bash
git add tests/test_integration.py
git commit -m "test: add integration test for full crawl workflow"
```

---


**Files:**
- Create: `crawler.py`

- [ ] **Step 1: Implement CLI with argparse**

```python
# crawler.py
#!/usr/bin/env python3
import argparse
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from webcrawler.config_loader import ConfigLoader
from webcrawler.spiders.generic_spider import GenericSpider

def main():
    parser = argparse.ArgumentParser(description='Distributed Web Crawler')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--urls', nargs='+', help='Seed URLs (overrides config)')
    parser.add_argument('--workers', type=int, help='Concurrent requests')
    parser.add_argument('--delay', type=float, help='Download delay in seconds')
    parser.add_argument('--depth', type=int, help='Max crawl depth')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Log level')
    
    args = parser.parse_args()
    
    # Load configuration
    loader = ConfigLoader(args.config)
    cli_overrides = {}
    if args.urls:
        cli_overrides['seed_urls'] = args.urls
    if args.workers:
        cli_overrides['concurrent_requests'] = args.workers
    if args.delay:
        cli_overrides['download_delay'] = args.delay
    if args.depth:
        cli_overrides['max_depth'] = args.depth
    if args.log_level:
        cli_overrides['log_level'] = args.log_level
    
    config = loader.load(cli_overrides)
    
    # Configure Scrapy settings
    settings = get_project_settings()
    settings.set('CONCURRENT_REQUESTS', config.get('concurrent_requests', 3))
    settings.set('DOWNLOAD_DELAY', config.get('download_delay', 1.0))
    settings.set('DOWNLOAD_TIMEOUT', config.get('timeout', 30))
    settings.set('RETRY_TIMES', config.get('retry_times', 3))
    settings.set('DATABASE_PATH', config.get('database_path', 'data/crawler.db'))
    settings.set('LOG_LEVEL', config.get('log_level', 'INFO'))
    settings.set('LOG_FILE', config.get('log_file', 'data/crawler.log'))
    
    # Start crawler
    process = CrawlerProcess(settings)
    process.crawl(
        GenericSpider,
        start_urls=config['seed_urls'],
        allowed_domains=config.get('allowed_domains', []),
        extraction_rules=config.get('extraction_rules', {}),
        max_depth=config.get('max_depth', 3)
    )
    process.start()

if __name__ == '__main__':
    main()
```

- [ ] **Step 2: Make crawler.py executable**

Run: `chmod +x crawler.py`

- [ ] **Step 3: Test CLI help**

Run: `python crawler.py --help`
Expected: Shows usage and all options

- [ ] **Step 4: Commit**

```bash
git add crawler.py
git commit -m "feat: add CLI entry point with config and argument parsing"
```

---


**Files:**
- Create: `webcrawler/spiders/generic_spider.py`
- Create: `tests/test_spider.py`

- [ ] **Step 1: Write test for spider parsing**

```python
# tests/test_spider.py
import json
from scrapy.http import HtmlResponse, Request
from webcrawler.spiders.generic_spider import GenericSpider

def test_spider_parses_page():
    spider = GenericSpider(
        start_urls=["http://example.com"],
        extraction_rules={"title": "h1::text"}
    )
    
    html = "<html><body><h1>Test Title</h1><a href='/page2'>Link</a></body></html>"
    response = HtmlResponse(url="http://example.com", body=html.encode('utf-8'))
    
    results = list(spider.parse(response))
    
    assert len(results) > 0
    item = results[0]
    assert item['url'] == "http://example.com"
    assert item['title'] == "Test Title"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_spider.py::test_spider_parses_page -v`
Expected: FAIL with "No module named 'webcrawler.spiders.generic_spider'"

- [ ] **Step 3: Implement GenericSpider (part 1)**

```python
# webcrawler/spiders/generic_spider.py
import json
import scrapy
from bs4 import BeautifulSoup
from webcrawler.items import CrawledPage

class GenericSpider(scrapy.Spider):
    name = 'generic'
    
    def __init__(self, start_urls=None, allowed_domains=None, extraction_rules=None, max_depth=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls or []
        self.allowed_domains = allowed_domains or []
        self.extraction_rules = extraction_rules or {}
        self.max_depth = max_depth
```

- [ ] **Step 4: Implement GenericSpider (part 2 - parse method)**

```python
    def parse(self, response):
        depth = response.meta.get('depth', 0)
        
        # Extract data using configured rules
        item = CrawledPage()
        item['url'] = response.url
        item['status_code'] = response.status
        item['depth'] = depth
        
        # Extract title
        title_selector = self.extraction_rules.get('title', 'title::text')
        title = response.css(title_selector).get()
        item['title'] = title.strip() if title else None
        
        # Extract text content
        soup = BeautifulSoup(response.text, 'lxml')
        for script in soup(["script", "style"]):
            script.decompose()
        text_content = soup.get_text(separator=' ', strip=True)
        item['text_content'] = text_content
        
        # Extract metadata
        metadata = {}
        desc_selector = self.extraction_rules.get('description', 'meta[name="description"]::attr(content)')
        description = response.css(desc_selector).get()
        if description:
            metadata['description'] = description
        item['metadata_json'] = json.dumps(metadata)
        
        yield item
        
        # Follow links if within depth limit
        if depth < self.max_depth:
            links_selector = self.extraction_rules.get('links', 'a::attr(href)')
            for link in response.css(links_selector).getall():
                yield response.follow(link, callback=self.parse, meta={'depth': depth + 1})
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_spider.py::test_spider_parses_page -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add webcrawler/spiders/generic_spider.py tests/test_spider.py
git commit -m "feat: add generic spider with configurable extraction"
```

---


**Files:**
- Create: `webcrawler/settings.py`

- [ ] **Step 1: Create Scrapy settings**

```python
# webcrawler/settings.py
BOT_NAME = 'webcrawler'

SPIDER_MODULES = ['webcrawler.spiders']
NEWSPIDER_MODULE = 'webcrawler.spiders'

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 3

DOWNLOAD_DELAY = 1.0

DOWNLOAD_TIMEOUT = 30

RETRY_TIMES = 3

ITEM_PIPELINES = {
    'webcrawler.pipelines.SQLitePipeline': 300,
}

DATABASE_PATH = 'data/crawler.db'

LOG_LEVEL = 'INFO'
LOG_FILE = 'data/crawler.log'

REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
```

- [ ] **Step 2: Commit**

```bash
git add webcrawler/settings.py
git commit -m "feat: add Scrapy settings with middleware and pipeline config"
```

---


**Files:**
- Create: `webcrawler/config_loader.py`
- Create: `tests/test_config_loader.py`
- Create: `config.yaml`

- [ ] **Step 1: Write test for config loading**

```python
# tests/test_config_loader.py
import pytest
from webcrawler.config_loader import ConfigLoader

def test_load_config_from_yaml(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text("""
seed_urls:
  - "http://example.com"
concurrent_requests: 3
download_delay: 1.0
""")
    
    loader = ConfigLoader(str(config_file))
    config = loader.load()
    
    assert config['seed_urls'] == ["http://example.com"]
    assert config['concurrent_requests'] == 3
    assert config['download_delay'] == 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_config_loader.py::test_load_config_from_yaml -v`
Expected: FAIL with "No module named 'webcrawler.config_loader'"

- [ ] **Step 3: Implement ConfigLoader**

```python
# webcrawler/config_loader.py
import yaml
import logging

logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self, config_path='config.yaml'):
        self.config_path = config_path
    
    def load(self, cli_overrides=None):
        """Load config from YAML and merge with CLI overrides."""
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if cli_overrides:
            config.update(cli_overrides)
        
        logger.info(f"Loaded configuration from {self.config_path}")
        return config
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_config_loader.py::test_load_config_from_yaml -v`
Expected: PASS

- [ ] **Step 5: Create default config.yaml**

```yaml
# config.yaml
seed_urls:
  - "http://example.com"

allowed_domains: []

max_depth: 3

concurrent_requests: 3

download_delay: 1.0

timeout: 30

retry_times: 3

extraction_rules:
  title: "h1::text"
  description: "meta[name='description']::attr(content)"
  links: "a::attr(href)"

database_path: "data/crawler.db"

log_file: "data/crawler.log"
log_level: "INFO"
```

- [ ] **Step 6: Commit**

```bash
git add webcrawler/config_loader.py tests/test_config_loader.py config.yaml
git commit -m "feat: add configuration loader with YAML support"
```

---


**Files:**
- Create: `webcrawler/pipelines.py`
- Create: `tests/test_pipeline.py`

- [ ] **Step 1: Write test for pipeline storage**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_pipeline.py::test_pipeline_stores_item -v`
Expected: FAIL with "No module named 'webcrawler.pipelines'"

- [ ] **Step 3: Implement SQLitePipeline**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_pipeline.py::test_pipeline_stores_item -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add webcrawler/pipelines.py tests/test_pipeline.py
git commit -m "feat: add SQLite pipeline for storing crawled data"
```

---


**Files:**
- Create: `webcrawler/items.py`

- [ ] **Step 1: Define Scrapy Item**

```python
# webcrawler/items.py
import scrapy

class CrawledPage(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text_content = scrapy.Field()
    metadata_json = scrapy.Field()
    status_code = scrapy.Field()
    depth = scrapy.Field()
```

- [ ] **Step 2: Commit**

```bash
git add webcrawler/items.py
git commit -m "feat: add item definitions for crawled pages"
```

---


**Files:**
- Create: `webcrawler/db_manager.py`
- Create: `tests/test_db_manager.py`

- [ ] **Step 1: Write test for database initialization**

```python
# tests/test_db_manager.py
import os
import sqlite3
import pytest
from webcrawler.db_manager import DatabaseManager

def test_initialize_database_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    db_manager = DatabaseManager(str(db_path))
    db_manager.initialize()
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    assert "crawled_pages" in tables
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_db_manager.py::test_initialize_database_creates_tables -v`
Expected: FAIL with "No module named 'webcrawler.db_manager'"

- [ ] **Step 3: Implement DatabaseManager**

```python
# webcrawler/db_manager.py
import sqlite3
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
    
    def initialize(self):
        """Create database schema with WAL mode for concurrent access."""
        conn = sqlite3.connect(self.db_path)
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
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_db_manager.py::test_initialize_database_creates_tables -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add webcrawler/db_manager.py tests/test_db_manager.py
git commit -m "feat: add database manager with schema initialization"
```

---


**Files:**
- Create: `requirements.txt`
- Create: `scrapy.cfg`
- Create: `webcrawler/__init__.py`
- Create: `webcrawler/spiders/__init__.py`
- Create: `tests/__init__.py`
- Create: `data/.gitkeep`

- [ ] **Step 1: Create requirements.txt**

```txt
scrapy>=2.11.0
beautifulsoup4>=4.12.0
pyyaml>=6.0
lxml>=4.9.0
pytest>=7.4.0
```

- [ ] **Step 2: Create scrapy.cfg**

```ini
[settings]
default = webcrawler.settings

[deploy]
project = webcrawler
```

- [ ] **Step 3: Create package markers**

```bash
touch webcrawler/__init__.py
touch webcrawler/spiders/__init__.py
touch tests/__init__.py
mkdir -p data
touch data/.gitkeep
```

- [ ] **Step 4: Install dependencies**

Run: `pip install -r requirements.txt`
Expected: All packages installed successfully

- [ ] **Step 5: Verify Scrapy installation**

Run: `scrapy version`
Expected: Output shows Scrapy 2.11.0 or higher

- [ ] **Step 6: Commit**

```bash
git add requirements.txt scrapy.cfg webcrawler/ tests/ data/.gitkeep
git commit -m "feat: initialize project structure and dependencies"
```

---


**New files to create:**

```
crawler/
├── config.yaml              # Default configuration with seed URLs and settings
├── crawler.py               # CLI entry point with argparse
├── scrapy.cfg               # Scrapy project configuration
├── webcrawler/
│   ├── __init__.py          # Package marker
│   ├── settings.py          # Scrapy settings (concurrency, delays, middleware)
│   ├── items.py             # Item definitions for scraped data
│   ├── pipelines.py         # SQLite storage pipeline
│   ├── config_loader.py     # YAML config loader with CLI overrides
│   ├── db_manager.py        # Database initialization and schema
│   └── spiders/
│       ├── __init__.py      # Package marker
│       └── generic_spider.py # Configurable spider with extraction rules
├── tests/
│   ├── __init__.py
│   ├── test_config_loader.py
│   ├── test_db_manager.py
│   ├── test_pipeline.py
│   └── test_spider.py
├── data/                    # Created at runtime
│   ├── crawler.db           # SQLite database
│   └── crawler.log          # Log file
├── requirements.txt         # Python dependencies
└── README.md                # Usage documentation
```

**Responsibilities:**
- `crawler.py`: Parse CLI args, load config, launch Scrapy crawler
- `config_loader.py`: Load YAML, merge with CLI overrides, validate
- `db_manager.py`: Create tables, manage connections, handle schema
- `items.py`: Define data structure for scraped content
- `pipelines.py`: Process items, store to SQLite, handle duplicates
- `generic_spider.py`: Fetch pages, extract data using config rules, follow links
- `settings.py`: Configure Scrapy behavior (concurrency, delays, middleware)

---

