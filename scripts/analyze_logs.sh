#!/bin/bash
# Log analysis using awk and sed

LOG_FILE="${1:-data/crawler.log}"

echo "=== Crawler Log Analysis ==="
echo ""

echo "Total log entries:"
wc -l "$LOG_FILE"

echo ""
echo "Errors by type:"
grep ERROR "$LOG_FILE" | awk '{print $NF}' | sort | uniq -c | sort -rn

echo ""
echo "Top 10 crawled domains:"
grep "Crawled" "$LOG_FILE" | sed -n 's/.*http[s]*:\/\/\([^\/]*\).*/\1/p' | sort | uniq -c | sort -rn | head -10

echo ""
echo "Status code distribution:"
grep "status" "$LOG_FILE" | awk '{print $NF}' | sort | uniq -c
