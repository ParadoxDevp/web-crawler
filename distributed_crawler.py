#!/usr/bin/env python3
"""CLI for distributed web crawler."""
import argparse
from webcrawler.distributed_crawler import DistributedCrawler
from webcrawler.analyzer import CrawlAnalyzer
from webcrawler.visualizer import CrawlVisualizer

def main():
    parser = argparse.ArgumentParser(description='Distributed Web Crawler')
    parser.add_argument('command', choices=['crawl', 'analyze', 'visualize'])
    parser.add_argument('--urls', nargs='+', help='Seed URLs')
    parser.add_argument('--depth', type=int, default=3, help='Max depth')
    parser.add_argument('--redis-host', default='localhost', help='Redis host')
    
    args = parser.parse_args()
    
    if args.command == 'crawl':
        crawler = DistributedCrawler(redis_host=args.redis_host)
        if args.urls:
            crawler.add_seed_urls(args.urls)
        crawler.start_crawl(max_depth=args.depth)
    elif args.command == 'analyze':
        analyzer = CrawlAnalyzer()
        print(analyzer.get_stats())
    elif args.command == 'visualize':
        viz = CrawlVisualizer()
        viz.plot_depth_distribution()

if __name__ == '__main__':
    main()
