# Distributed Web Crawler

A clean, modular web crawler with real-time dashboard, bloom filter duplicate detection, and distributed worker support.

## Features

- **Real-time Web Dashboard** - Monitor crawling at http://localhost:5000
- **Bloom Filter** - Memory-efficient duplicate detection
- **Distributed Workers** - Celery + Redis for parallel crawling
- **Data Analysis** - Pandas statistics and matplotlib charts
- **SQLAlchemy ORM** - Robust database layer
- **Config Support** - YAML configuration with CLI overrides
- **Clean Console** - Progress indicators without spam

## Architecture

4 core modules (~200 lines total):
- `core_crawler.py` - Crawling logic + bloom filter
- `data_ingestion.py` - SQLAlchemy database operations
- `distributed_manager.py` - Redis queue + Celery tasks
- `visualization.py` - Pandas analysis + matplotlib charts
- `web_dashboard.py` - Flask real-time dashboard

## Installation

```bash
# Clone and setup
git clone <repo-url>
cd final-project
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Default Crawl
```bash
python main.py
```
Uses `config.yaml` settings, starts dashboard at http://localhost:5000

### Custom Crawl
```bash
python main.py crawl --urls https://python.org --depth 2
```

### Analyze Data
```bash
python main.py analyze
```
Shows statistics, generates chart, exports CSV

### Clear Data
```bash
python main.py clear
```

### Distributed Crawl
```bash
# Terminal 1: Start workers
celery -A distributed_manager worker --loglevel=info --concurrency=4

# Terminal 2: Run crawler
python main.py distributed --urls https://github.com
```

## Dashboard

Visit http://localhost:5000 to see:
- Real-time statistics (updates every 2s)
- Depth distribution chart
- Recent crawled pages
- Click any row to see full captured data

## Configuration

Edit `config.yaml`:
```yaml
seed_urls:
  - "https://python.org"
  - "https://github.com"
max_depth: 3
```

## Output

Console shows:
```
🌐 Starting dashboard at http://localhost:5000
[Worker] Crawling: https://python.org (depth=0)
✓ Crawled: https://python.org [200]
✓ Saved: https://python.org
✓ Crawl complete: {'crawled': 5, 'failed': 0, 'duplicates': 2}
📊 View dashboard: http://localhost:5000
```

## License

Educational use only.
