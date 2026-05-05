# Web Crawler

A configurable web crawler built with Scrapy that extracts structured data from websites and stores it in SQLite.

## Features

- **Configurable crawling**: YAML-based configuration for URLs, depth, concurrency, and extraction rules
- **CLI overrides**: Command-line arguments override config file settings
- **SQLite storage**: Persistent storage with WAL mode for concurrent access
- **Depth control**: Limit crawl depth to prevent excessive crawling
- **Rate limiting**: Configurable download delays and concurrent requests
- **Retry logic**: Automatic retry on failures
- **Robots.txt compliance**: Respects website crawling policies
- **Structured extraction**: CSS selector-based data extraction
- **Comprehensive logging**: File and console logging with configurable levels

## Installation

1. Clone the repository:
```bash
cd /home/nihal/MU/scripting_wkshp/final-project
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run with default configuration:
```bash
python crawler.py
```

### CLI Options

```bash
python crawler.py --config config.yaml \
                  --urls http://example.com http://example.org \
                  --workers 5 \
                  --delay 2.0 \
                  --depth 2 \
                  --log-level INFO
```

**Available options:**
- `--config`: Path to configuration file (default: `config.yaml`)
- `--urls`: Override seed URLs (space-separated)
- `--workers`: Number of concurrent requests
- `--delay`: Download delay in seconds
- `--depth`: Maximum crawl depth
- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Configuration

Edit `config.yaml` to customize crawler behavior:

```yaml
# Seed URLs to start crawling
seed_urls:
  - "http://example.com"

# Restrict crawling to specific domains (empty = no restriction)
allowed_domains: []

# Maximum depth to crawl
max_depth: 3

# Number of concurrent requests
concurrent_requests: 3

# Delay between requests (seconds)
download_delay: 1.0

# Request timeout (seconds)
timeout: 30

# Number of retry attempts
retry_times: 3

# CSS selectors for data extraction
extraction_rules:
  title: "h1::text"
  description: "meta[name='description']::attr(content)"
  links: "a::attr(href)"

# Database location
database_path: "data/crawler.db"

# Log file location
log_file: "data/crawler.log"

# Logging level
log_level: "INFO"
```

### Extraction Rules

Extraction rules use CSS selectors with Scrapy syntax:
- `::text` - Extract text content
- `::attr(name)` - Extract attribute value
- Multiple selectors return lists

Examples:
```yaml
extraction_rules:
  title: "h1::text"
  meta_description: "meta[name='description']::attr(content)"
  all_links: "a::attr(href)"
  paragraphs: "p::text"
  images: "img::attr(src)"
```

## Database Query Examples

The crawler stores data in SQLite at `data/crawler.db`. Access it using:

```bash
sqlite3 data/crawler.db
```

### Useful Queries

**View all crawled pages:**
```sql
SELECT url, title, status_code, depth, crawled_at 
FROM crawled_pages 
ORDER BY crawled_at DESC;
```

**Count pages by depth:**
```sql
SELECT depth, COUNT(*) as page_count 
FROM crawled_pages 
GROUP BY depth 
ORDER BY depth;
```

**Find pages with specific title:**
```sql
SELECT url, title 
FROM crawled_pages 
WHERE title LIKE '%search term%';
```

**Get recent crawls:**
```sql
SELECT url, title, crawled_at 
FROM crawled_pages 
WHERE crawled_at > datetime('now', '-1 hour')
ORDER BY crawled_at DESC;
```

**View metadata:**
```sql
SELECT url, metadata_json 
FROM crawled_pages 
WHERE metadata_json IS NOT NULL;
```

**Export to CSV:**
```sql
.mode csv
.output results.csv
SELECT * FROM crawled_pages;
.output stdout
```

### Database Schema

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
```

## Testing

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_config_loader.py
pytest tests/test_db_manager.py
pytest tests/test_spider.py
pytest tests/test_pipeline.py
pytest tests/test_integration.py
```

Run with verbose output:
```bash
pytest -v
```

Run with coverage:
```bash
pytest --cov=webcrawler
```

## Logs Location

Logs are stored in two locations:

1. **File logs**: `data/crawler.log` (configurable in `config.yaml`)
   - Persistent logs for all crawl sessions
   - Rotation recommended for production use

2. **Console output**: Real-time logging to terminal
   - Controlled by `--log-level` CLI argument or `log_level` in config

**View logs:**
```bash
tail -f data/crawler.log
```

**Filter by level:**
```bash
grep ERROR data/crawler.log
grep WARNING data/crawler.log
```

## Project Structure

```
.
├── config.yaml              # Main configuration file
├── crawler.py               # CLI entry point
├── requirements.txt         # Python dependencies
├── scrapy.cfg              # Scrapy project config
├── data/                   # Data directory
│   ├── crawler.db          # SQLite database
│   └── crawler.log         # Log file
├── webcrawler/             # Main package
│   ├── __init__.py
│   ├── config_loader.py    # Configuration management
│   ├── db_manager.py       # Database operations
│   ├── items.py            # Scrapy items
│   ├── pipelines.py        # Data processing pipeline
│   ├── settings.py         # Scrapy settings
│   └── spiders/
│       └── generic_spider.py  # Main spider
└── tests/                  # Test suite
    ├── test_config_loader.py
    ├── test_db_manager.py
    ├── test_spider.py
    ├── test_pipeline.py
    └── test_integration.py
```

## License

This project is provided as-is for educational purposes.
