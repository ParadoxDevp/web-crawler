#!/bin/bash
# Extract data from crawler database using jq

DB_FILE="${1:-data/crawler.db}"

echo "=== Extracting JSON data from crawler database ==="

# Export to JSON
sqlite3 "$DB_FILE" <<EOF | jq '.'
.mode json
SELECT url, title, status_code, depth, metadata_json FROM crawled_pages LIMIT 10;
EOF

echo ""
echo "Extract specific fields:"
sqlite3 "$DB_FILE" <<EOF | jq '.[] | {url, title}'
.mode json
SELECT url, title FROM crawled_pages WHERE status_code = 200;
EOF
