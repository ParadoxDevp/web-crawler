#!/usr/bin/env python3
"""Main CLI for distributed web crawler."""
import argparse
import yaml
import threading
from core_crawler import CoreCrawler
from distributed_manager import DistributedManager, crawl_task
from data_ingestion import DataIngestion
from visualization import Visualization
from web_dashboard import start_dashboard
import time


def load_config(config_path='config.yaml'):
    """Load config from YAML."""
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except:
        return {'seed_urls': ['http://example.com'], 'max_depth': 3}


def main():
    parser = argparse.ArgumentParser(description='Distributed Web Crawler')
    parser.add_argument('mode', nargs='?', default='crawl', choices=['crawl', 'distributed', 'analyze', 'clear'])
    parser.add_argument('--urls', nargs='+', help='Seed URLs')
    parser.add_argument('--depth', type=int, help='Max depth')
    parser.add_argument('--config', default='config.yaml', help='Config file')
    
    args = parser.parse_args()
    config = load_config(args.config)
    
    urls = args.urls or config.get('seed_urls', ['http://example.com'])
    depth = args.depth or config.get('max_depth', 3)
    
    # Start web dashboard in background
    print("🌐 Starting dashboard at http://localhost:5000")
    dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
    dashboard_thread.start()
    time.sleep(1)
    
    if args.mode == 'crawl':
        crawler = CoreCrawler(max_depth=depth)
        db = DataIngestion()
        
        for url in urls:
            result = crawler.crawl(url)
            if result:
                db.save(result)
                for link in result.get('links', [])[:5]:
                    sub_result = crawler.crawl(link, depth=1)
                    if sub_result:
                        db.save(sub_result)
        
        print(f"\n✓ Crawl complete: {crawler.stats}")
        
    elif args.mode == 'distributed':
        try:
            manager = DistributedManager()
            manager.add_urls(urls)
            
            while manager.queue_size() > 0:
                url = manager.get_next_url()
                if url:
                    print(f"→ Dispatching: {url}")
                    crawl_task.delay(url)
                    time.sleep(0.5)
            
            print("\n✓ All tasks dispatched")
        except Exception as e:
            print("\n✗ Error: Redis server not running")
            print("Start Redis with: redis-server")
            print("Or use 'crawl' mode instead")
            return
        
    elif args.mode == 'analyze':
        viz = Visualization()
        viz.get_stats()
        viz.plot_depth_chart()
        viz.export_csv()
        
    elif args.mode == 'clear':
        import os
        if os.path.exists('data/crawler.db'):
            os.remove('data/crawler.db')
            print("✓ Database cleared")
        else:
            print("⊘ No database found")
        return
    
    print("\n📊 View dashboard: http://localhost:5000")
    input("Press Enter to exit...")


if __name__ == '__main__':
    main()
