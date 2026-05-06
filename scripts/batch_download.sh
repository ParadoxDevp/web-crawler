#!/bin/bash
# Batch download using wget/curl

URLS_FILE="${1:-urls.txt}"
OUTPUT_DIR="${2:-data/downloads}"

mkdir -p "$OUTPUT_DIR"

echo "=== Batch Downloader ==="
echo "Reading URLs from: $URLS_FILE"
echo "Output directory: $OUTPUT_DIR"

while IFS= read -r url; do
    echo "Downloading: $url"
    wget -q -P "$OUTPUT_DIR" "$url" || curl -s -o "$OUTPUT_DIR/$(basename $url)" "$url"
done < "$URLS_FILE"

echo "Download complete. Files saved to $OUTPUT_DIR"
