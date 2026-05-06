"""Tests for bloom filter."""
import pytest
from webcrawler.bloom_filter import URLBloomFilter

def test_bloom_filter_add_contains():
    bloom = URLBloomFilter(capacity=1000)
    
    bloom.add('http://example.com')
    assert bloom.contains('http://example.com')
    assert not bloom.contains('http://notadded.com')

def test_bloom_filter_length():
    bloom = URLBloomFilter(capacity=1000)
    bloom.add('http://test1.com')
    bloom.add('http://test2.com')
    
    assert len(bloom) == 2
