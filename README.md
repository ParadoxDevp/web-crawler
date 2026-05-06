# Distributed Web Crawler

A production-ready distributed web crawler with real-time monitoring dashboard, bloom filter duplicate detection, and multi-worker support.

## Features

### Core Crawling
- **Bloom Filter Duplicate Detection** - Memory-efficient duplicate URL detection (1M URLs, 0.1% error rate)
- **Configurable Depth Control** - Limit crawl depth to prevent excessive crawling
- **Rate Limiting** - Configurable delays between requests
- **Retry Logic** - Automatic retry on failures with exponential backoff
- **BeautifulSoup Parsing** - Extract text content and links from HTML

### Distributed Architecture
- **Redis Queue** - Priority-based distributed URL queue
- **Celery Workers** - Parallel task processing across multiple workers
- **SQLAlchemy ORM** - Robust database layer with SQLite support
- **Concurrent Crawling** - Multiple workers crawl simultaneously

### Data Analysis
- **Pandas Integration** - Statistical analysis of crawled data
- **Matplotlib Visualization** - Depth distribution charts
- **CSV Export** - Export results for further analysis
- **Real-time Statistics** - Live crawl metrics

### Web Dashboard
- **Real-time Monitoring** - Auto-updates every 2 seconds
- **Interactive UI** - Click any page to see full captured data
- **Depth Charts** - Visual representation of crawl depth
- **Status Tracking** - Monitor crawl progress live

## Architecture

### Core Modules

**core_crawler.py** (~40 lines)
- HTTP requests with timeout handling
- BeautifulSoup HTML parsing
- Bloom filter duplicate detection
- Link extraction and URL normalization
- Console progress indicators

**data_ingestion.py** (~55 lines)
- SQLAlchemy ORM models
- Database initialization
- CRUD operations
- Duplicate checking before insert
- Transaction management

**distributed_manager.py** (~30 lines)
- Redis priority queue implementation
- Celery task definitions
- URL distribution across workers
- Queue size monitoring

**visualization.py** (~40 lines)
- Pandas DataFrame operations
- Statistical calculations
- Matplotlib chart generation
- CSV export functionality

**web_dashboard.py** (~30 lines)
- Flask web server
- REST API endpoints
- Real-time data updates
- Chart image serving

**main.py** (~80 lines)
- CLI argument parsing
- Config file loading
- Dashboard thread management
- Mode routing (crawl/analyze/clear)

## Installation

### Prerequisites
- Python 3.8+
- Redis server (for distributed mode)

### Setup Steps

1. **Clone the repository**
```bash
git clone <repo-url>
cd final-project
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Optional: Install Redis (for distributed mode)**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Start Redis
redis-server
```

## Usage

### 1. Default Crawl (Recommended)

```bash
python main.py
```

**What it does:**
- Loads URLs from `config.yaml`
- Starts dashboard at http://localhost:5000
- Crawls all seed URLs
- Saves data to SQLite database
- Shows progress in console

**Console Output:**
```
🌐 Starting dashboard at http://localhost:5000
[Worker] Crawling: https://python.org (depth=0)
✓ Crawled: https://python.org [200]
✓ Saved: https://python.org
✓ Crawl complete: {'crawled': 5, 'failed': 0, 'duplicates': 2}
📊 View dashboard: http://localhost:5000
```

### 2. Custom Crawl

```bash
python main.py crawl --urls https://python.org https://github.com --depth 2
```

**Options:**
- `--urls` - Override seed URLs
- `--depth` - Maximum crawl depth (default: 3)

### 3. Analyze Data

```bash
python main.py analyze
```

**What it does:**
- Calculates statistics (total pages, avg depth, status codes)
- Generates depth distribution chart (`data/depth_chart.png`)
- Exports data to CSV (`data/results.csv`)

**Output:**
```
=== Crawl Statistics ===
Total Pages: 23
Average Depth: 1.20
Status Codes: {200: 22, 404: 1}
✓ Chart saved: data/depth_chart.png
✓ Exported 23 rows to data/results.csv
```

### 4. Clear Database

```bash
python main.py clear
```

Removes `data/crawler.db` - next crawl starts fresh.

### 5. Distributed Crawl

**Terminal 1: Start Celery workers**
```bash
celery -A distributed_manager worker --loglevel=info --concurrency=4
```

**Terminal 2: Run crawler**
```bash
python main.py distributed --urls https://github.com
```

**What it does:**
- Distributes URLs across multiple Celery workers
- Workers process URLs in parallel
- Results stored in shared database

## Web Dashboard

Access at **http://localhost:5000** (auto-starts with any command)

### Features

**Real-time Statistics**
- Total pages crawled
- Average depth
- Status code distribution
- Updates every 2 seconds

**Depth Distribution Chart**
- Visual bar chart showing pages per depth level
- Auto-generated from crawl data

**Recent Pages Table**
- Last 20 crawled pages
- Shows URL, title, and depth
- Click any row to see full details

**Page Details Modal**
- Full page title
- Clickable URL (opens in new tab)
- HTTP status code
- Crawl depth
- Complete captured text content (scrollable)

## Configuration

Edit `config.yaml` to customize crawler behavior:

```yaml
# Seed URLs to start crawling
seed_urls:
  - "https://httpbin.org/html"
  - "https://www.python.org"
  - "https://github.com"

# Maximum crawl depth
max_depth: 3
```

## Database

**Location:** `data/crawler.db`

**Schema:**
```sql
CREATE TABLE crawled_pages (
    id INTEGER PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    title TEXT,
    text_content TEXT,
    status_code INTEGER,
    depth INTEGER,
    crawled_at TIMESTAMP
);
```

## Project Structure

```
.
├── core_crawler.py          # Crawling logic + bloom filter
├── data_ingestion.py        # SQLAlchemy ORM + database
├── distributed_manager.py   # Redis queue + Celery tasks
├── visualization.py         # Pandas analysis + charts
├── web_dashboard.py         # Flask dashboard
├── main.py                  # CLI entry point
├── config.yaml              # Configuration
├── requirements.txt         # Dependencies
└── templates/
    └── dashboard.html       # Dashboard UI
```

## Dependencies

- **requests** - HTTP requests
- **beautifulsoup4** - HTML parsing
- **pybloom-live** - Bloom filter
- **sqlalchemy** - Database ORM
- **pandas** - Data analysis
- **matplotlib** - Charts
- **flask** - Web dashboard
- **redis** - Distributed queue
- **celery** - Task distribution

## License

Educational use only.
