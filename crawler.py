#!/usr/bin/env python3
"""CLI entry point for the web crawler."""
import argparse
import logging
import sys
from scrapy.crawler import CrawlerProcess
from webcrawler.config_loader import ConfigLoader
from webcrawler.spiders.generic_spider import GenericSpider

def main():
    parser = argparse.ArgumentParser(description='Configurable web crawler')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--urls', nargs='+', help='Override seed URLs')
    parser.add_argument('--workers', type=int, help='Number of concurrent requests')
    parser.add_argument('--delay', type=float, help='Download delay in seconds')
    parser.add_argument('--depth', type=int, help='Maximum crawl depth')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], help='Logging level')
    
    args = parser.parse_args()
    
    # Build CLI overrides
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
    
    # Load configuration
    try:
        loader = ConfigLoader(args.config)
        config = loader.load(cli_overrides)
    except Exception as e:
        print(f"Error loading config: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Configure Scrapy settings
    settings = {
        'CONCURRENT_REQUESTS': config.get('concurrent_requests', 3),
        'DOWNLOAD_DELAY': config.get('download_delay', 1.0),
        'DOWNLOAD_TIMEOUT': config.get('timeout', 30),
        'RETRY_TIMES': config.get('retry_times', 3),
        'DATABASE_PATH': config.get('database_path', 'data/crawler.db'),
        'LOG_LEVEL': config.get('log_level', 'INFO'),
        'LOG_FILE': config.get('log_file', 'data/crawler.log'),
        'ROBOTSTXT_OBEY': True,
        'ITEM_PIPELINES': {'webcrawler.pipelines.SQLitePipeline': 300},
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
    }
    
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
