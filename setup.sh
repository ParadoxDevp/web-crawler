#!/bin/bash
# Setup script for distributed web crawler

echo "=== Distributed Web Crawler Setup ==="

# Check Python version
python3 --version || { echo "Python 3.8+ required"; exit 1; }

# Check Redis
redis-cli ping > /dev/null 2>&1 || { echo "Redis not running. Start with: redis-server"; exit 1; }

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p data scripts

# Initialize database
python3 -c "from webcrawler.models import get_engine, init_db; init_db(get_engine())"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Start Celery workers: celery -A webcrawler.celery_app worker --loglevel=info"
echo "2. Run crawler: python distributed_crawler.py crawl --urls http://example.com"
