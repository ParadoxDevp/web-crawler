# Distributed Web Crawler Design Specification

**Date:** 2026-05-06  
**Project:** Distributed Web Crawler  
**Purpose:** General web scraping with concurrent workers, duplicate detection, and structured data extraction

## Overview

A small-scale distributed web crawler built on Scrapy framework for crawling multiple websites concurrently, extracting structured data, text content, and metadata while respecting robots.txt and rate limiting policies.

## Requirements Summary

- **Scale:** 2-5 concurrent workers on single machine
- **Use Case:** General web scraping for data collection
- **Data Extraction:** Structured data (titles, fields), text content, and metadata/links
- **Storage:** SQLite database
- **Politeness:** robots.txt compliance + basic request delays
- **Retry Logic:** Simple retry (3 attempts) for failed requests
- **Interface:** YAML config file with CLI argument overrides

## Architecture

### Framework Choice: Scrapy

Using Scrapy provides:
- Built-in robots.txt compliance via RobotsTxtMiddleware
- Native duplicate URL filtering
- Asynchronous I/O for efficient concurrent requests
- Retry middleware with configurable attempts
- Priority queue scheduler
- Extensive middleware ecosystem

### Core Components

1. **Generic Spider** (`spiders/generic_spider.py`)
   - Configurable spider accepting URL patterns and extraction rules
   - Uses CSS selectors or XPath for data extraction
   - Extracts: title, text content, metadata, outbound links
   - Respects domain restrictions from config

2. **Item Pipeline** (`pipelines.py`)
   - Receives extracted items from spider
   - Cleans and validates data
   - Stores to SQLite database
   - Handles duplicate URLs gracefully

3. **SQLite Database** (`data/crawler.db`)
   - Persistent storage for crawled data
   - Schema detailed below

4. **Configuration System**
   - YAML config file for defaults
   - CLI arguments override config values
   - Scrapy settings integration

5. **Middleware Stack**
   - RobotsTxtMiddleware: robots.txt compliance
   - RetryMiddleware: Handle failures with retries
   - DownloadDelayMiddleware: Rate limiting

### Data Flow

1. Load seed URLs from config file or CLI
2. Spider fetches pages respecting robots.txt and download delays
3. Extract structured data, text content, and links using configured selectors
4. Pipeline processes and stores results in SQLite
5. Discovered URLs added to Scrapy's scheduler (duplicate filtering automatic)
6. Process continues until queue empty or max depth reached

## Database Schema

### Table: crawled_pages

Primary storage for all crawled content.

```sql
CREATE TABLE crawled_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    text_content TEXT,
    metadata_json TEXT,
    crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_code INTEGER,
    depth INTEGER
);

CREATE INDEX idx_url ON crawled_pages(url);
CREATE INDEX idx_crawled_at ON crawled_pages(crawled_at);
```

### Table: crawl_stats (optional)

Track crawl statistics for monitoring.

```sql
CREATE TABLE crawl_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crawl_started TIMESTAMP,
    crawl_finished TIMESTAMP,
    pages_crawled INTEGER,
    pages_failed INTEGER,
    items_scraped INTEGER
);
```

## Configuration

### YAML Configuration File (config.yaml)

```yaml
# Seed URLs to start crawling
seed_urls:
  - "http://example.com"
  - "http://test.com"

# Optional: Restrict crawling to specific domains
allowed_domains:
  - "example.com"
  - "test.com"

# Crawl depth limit (0 = seed URLs only, None = unlimited)
max_depth: 3

# Number of concurrent requests (2-5 recommended)
concurrent_requests: 3

# Delay between requests to same domain (seconds)
download_delay: 1.0

# Request timeout (seconds)
timeout: 30

# Number of retry attempts for failed requests
retry_times: 3

# Extraction rules using CSS selectors or XPath
extraction_rules:
  title: "h1::text"
  description: "meta[name='description']::attr(content)"
  links: "a::attr(href)"
  
# Database path
database_path: "data/crawler.db"

# Log file path
log_file: "data/crawler.log"
log_level: "INFO"
```

### CLI Interface

```bash
# Use default config.yaml
python crawler.py

# Specify custom config file
python crawler.py --config custom.yaml

# Override specific settings
python crawler.py --workers 5 --delay 2 --depth 5

# Provide seed URLs directly (overrides config)
python crawler.py --urls "http://example.com" "http://test.com"

# Set log level
python crawler.py --log-level DEBUG
```

## Project Structure

```
crawler/
├── config.yaml              # Default configuration
├── crawler.py               # Main entry point (CLI)
├── spiders/
│   └── generic_spider.py    # Configurable spider
├── pipelines.py             # SQLite storage pipeline
├── items.py                 # Scrapy item definitions
├── settings.py              # Scrapy settings
├── requirements.txt         # Python dependencies
├── README.md                # Usage documentation
└── data/
    ├── crawler.db           # SQLite database (created at runtime)
    └── crawler.log          # Log file (created at runtime)
```

## Error Handling

### HTTP Errors
- **4xx errors (Client errors):** Retry up to 3 times, then log and skip
- **5xx errors (Server errors):** Retry up to 3 times with same delay
- **Timeouts:** Retry up to 3 times, configurable timeout (default 30s)
- **Connection errors:** Retry up to 3 times, then log and skip

### Parse Errors
- Log error with URL and exception details
- Skip problematic page
- Continue crawling other URLs

### robots.txt Failures
- If robots.txt cannot be fetched, assume all paths disallowed
- Log warning and skip domain

### Database Errors
- Duplicate URL inserts: Log and skip (already crawled)
- Connection errors: Retry operation, fail gracefully if persistent
- Schema errors: Fail fast with clear error message

## Logging and Monitoring

### Logging
- **Log file:** `data/crawler.log` with automatic rotation
- **Log levels:** DEBUG, INFO, WARNING, ERROR
- **Console output:** Progress indicators and summary stats
- **Logged events:**
  - Crawl start/stop
  - Pages fetched (URL, status code)
  - Errors and retries
  - Items scraped and stored
  - robots.txt compliance actions

### Statistics
Scrapy's built-in stats collector tracks:
- Total requests sent
- Responses received by status code
- Items scraped
- Errors encountered
- Average response time
- Crawl duration

### Monitoring Commands
```bash
# Check crawl progress (query SQLite)
sqlite3 data/crawler.db "SELECT COUNT(*) FROM crawled_pages;"

# View recent crawls
sqlite3 data/crawler.db "SELECT url, status_code, crawled_at FROM crawled_pages ORDER BY crawled_at DESC LIMIT 10;"

# Check error rate from logs
grep ERROR data/crawler.log | wc -l
```

## Graceful Shutdown

- **Ctrl+C:** Initiates graceful shutdown
- **Behavior:**
  - Stop accepting new URLs from scheduler
  - Allow in-progress requests to complete
  - Save statistics to database
  - Close database connections cleanly
  - Write final log entry

## Dependencies

```
scrapy>=2.11.0
beautifulsoup4>=4.12.0
pyyaml>=6.0
lxml>=4.9.0
```

Standard library modules:
- sqlite3
- argparse
- logging

## Testing Strategy

### Unit Tests
- Spider extraction logic with mock HTML
- Pipeline data validation and storage
- Configuration loading and CLI parsing

### Integration Tests
- End-to-end crawl with local test server
- Database operations under concurrent load
- robots.txt compliance verification

### Manual Testing
- Crawl small public websites (with permission)
- Verify duplicate detection
- Test graceful shutdown
- Validate extracted data quality

## Future Enhancements (Out of Scope)

- Bloom filter for more efficient duplicate detection at scale
- Distributed crawling across multiple machines (Redis queue)
- JavaScript rendering support (Scrapy-Splash integration)
- Adaptive rate limiting based on server response
- Web UI for monitoring and control
- Export to multiple formats (CSV, JSON, Parquet)

## Success Criteria

1. Successfully crawl 2-5 websites concurrently
2. Respect robots.txt and rate limits
3. Extract structured data, text, and metadata as configured
4. Store results in SQLite without data loss
5. Handle errors gracefully with retries
6. Provide clear logging and statistics
7. Support config file and CLI overrides
8. Complete graceful shutdown on interrupt

## Implementation Notes

- Keep extraction rules simple and configurable
- Prioritize code clarity over premature optimization
- Use Scrapy's built-in features rather than reinventing
- Ensure SQLite WAL mode for better concurrent access
- Document all configuration options clearly
