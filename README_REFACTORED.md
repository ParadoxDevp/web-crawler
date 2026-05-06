# Distributed Web Crawler - Refactored

Clean, modular architecture with 4 core files and console visibility.

## Architecture

```
core_crawler.py       → All crawling logic (bloom filter, requests, parsing)
distributed_manager.py → Worker orchestration (Redis queue, Celery tasks)
data_ingestion.py     → Database operations (SQLAlchemy ORM)
visualization.py      → Analysis & charts (pandas, matplotlib)
main.py              → CLI interface
```

## Quick Start

### 1. Single-Process Crawl
```bash
python main.py crawl --urls http://example.com --depth 2
```

Console output:
```
✓ Crawled: http://example.com [200]
✓ Saved: http://example.com
✓ Crawl complete: {'crawled': 5, 'failed': 0, 'duplicates': 2}
```

### 2. Distributed Crawl

Start workers:
```bash
celery -A distributed_manager worker --loglevel=info --concurrency=4
```

Run crawler:
```bash
python main.py distributed --urls http://example.com http://test.com
```

Console output:
```
✓ Added 2 URLs to queue
→ Dispatching: http://example.com
[Worker] Crawling: http://example.com (depth=0)
✓ Crawled: http://example.com [200]
```

### 3. Analyze Data
```bash
python main.py analyze
```

Console output:
```
=== Crawl Statistics ===
Total Pages: 15
Average Depth: 1.20
Status Codes: {200: 14, 404: 1}
```

### 4. Visualize
```bash
python main.py visualize
```

Console output:
```
✓ Chart saved: data/depth_chart.png
✓ Exported 15 rows to data/results.csv
```

## Module Details

**core_crawler.py** (40 lines)
- Bloom filter duplicate detection
- HTTP requests with BeautifulSoup
- Console progress indicators

**distributed_manager.py** (30 lines)
- Redis priority queue
- Celery task definitions
- Worker coordination

**data_ingestion.py** (35 lines)
- SQLAlchemy models
- Save/retrieve operations
- Error handling

**visualization.py** (40 lines)
- Pandas statistics
- Matplotlib charts
- CSV export

## Console Visibility

All operations print to console:
- ✓ Success messages (green checkmark)
- ✗ Error messages (red X)
- → Progress indicators (arrow)
- [Worker] Worker activity logs
