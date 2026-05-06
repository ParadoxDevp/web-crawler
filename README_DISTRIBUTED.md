# Distributed Web Crawler

A production-ready distributed web crawler with multiple concurrent workers, Redis-based queue, bloom filter duplicate detection, and comprehensive data analysis tools.

## Features

### Core Crawling
- **Distributed Architecture**: Multiple Celery workers for parallel crawling
- **Redis Queue**: Distributed priority queue for URL management
- **Bloom Filter**: Memory-efficient duplicate detection (1M URLs, 0.1% error rate)
- **Scrapy Framework**: Built-in robots.txt compliance and rate limiting
- **SQLAlchemy ORM**: Robust database layer with SQLite/PostgreSQL support

### Data Analysis
- **Pandas Integration**: Statistical analysis of crawled data
- **Matplotlib Visualization**: Depth distribution and crawl metrics
- **NetworkX**: Network graph analysis of site structure
- **CSV Export**: Easy data export for further analysis

### Network Analysis
- **Scapy Integration**: Packet capture and network traffic analysis
- **HTTP/HTTPS Monitoring**: Track crawler network behavior

### Shell Tools
- **Log Analysis**: awk/sed scripts for log processing
- **Batch Downloads**: wget/curl integration for bulk operations
- **JSON Extraction**: jq-based data extraction from database

## Installation

### Prerequisites
- Python 3.8+
- Redis server
- Optional: PostgreSQL for production use

### Setup

```bash
# Install Redis
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                  # macOS

# Start Redis
redis-server

# Install Python dependencies
pip install -r requirements.txt
```

## Usage

### 1. Scrapy-based Crawler (Single Process)

```bash
python crawler.py --urls http://example.com --depth 3
```

### 2. Distributed Crawler (Multiple Workers)

Start Celery workers:
```bash
celery -A webcrawler.celery_app worker --loglevel=info --concurrency=4
```

Run distributed crawler:
```bash
python distributed_crawler.py crawl --urls http://example.com http://test.com --depth 3
```

### 3. Data Analysis

```bash
# Get statistics
python distributed_crawler.py analyze

# Generate visualizations
python distributed_crawler.py visualize
```

### 4. Shell Tools

```bash
# Analyze logs
./scripts/analyze_logs.sh data/crawler.log

# Batch download
./scripts/batch_download.sh urls.txt data/downloads

# Extract JSON data
./scripts/extract_json.sh data/crawler.db
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Redis     │────▶│ Celery Worker│────▶│  Database   │
│   Queue     │     │   (Worker 1)  │     │  (SQLite)   │
└─────────────┘     └──────────────┘     └─────────────┘
      │             ┌──────────────┐            │
      └────────────▶│ Celery Worker│────────────┘
                    │   (Worker 2)  │
                    └──────────────┘
                    ┌──────────────┐
                    │ Bloom Filter │
                    │  (Dedup)     │
                    └──────────────┘
```

## Configuration

Edit `config.yaml`:

```yaml
seed_urls:
  - "http://example.com"

max_depth: 3
concurrent_requests: 5
download_delay: 1.0

# Redis configuration
redis_host: "localhost"
redis_port: 6379

# Bloom filter settings
bloom_capacity: 1000000
bloom_error_rate: 0.001
```

## Components

### Python Modules
- `webcrawler/redis_queue.py` - Distributed priority queue
- `webcrawler/bloom_filter.py` - Duplicate detection
- `webcrawler/celery_app.py` - Distributed task system
- `webcrawler/models.py` - SQLAlchemy ORM models
- `webcrawler/analyzer.py` - Data analysis with pandas
- `webcrawler/visualizer.py` - Visualization tools
- `webcrawler/network_analyzer.py` - Network traffic analysis

### Shell Scripts
- `scripts/analyze_logs.sh` - Log analysis (awk/sed)
- `scripts/batch_download.sh` - Batch downloads (wget/curl)
- `scripts/extract_json.sh` - JSON extraction (jq)

## Testing

```bash
pytest tests/ -v
```

## Database Queries

```sql
-- View crawl statistics
SELECT COUNT(*) as total, AVG(depth) as avg_depth FROM crawled_pages;

-- Top domains
SELECT SUBSTR(url, 1, INSTR(SUBSTR(url, 9), '/')+8) as domain, COUNT(*) 
FROM crawled_pages GROUP BY domain ORDER BY COUNT(*) DESC LIMIT 10;
```

## Performance

- **Throughput**: 100-500 pages/minute (depends on workers)
- **Memory**: ~50MB base + 1.2MB per 100K URLs in bloom filter
- **Storage**: ~1KB per page in database

## License

Educational use only.
