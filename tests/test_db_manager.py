import os
import sqlite3
import pytest
from webcrawler.db_manager import DatabaseManager

def test_initialize_database_creates_tables(tmp_path):
    db_path = tmp_path / "test.db"
    db_manager = DatabaseManager(str(db_path))
    db_manager.initialize()
    
    with sqlite3.connect(str(db_path)) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        assert "crawled_pages" in tables
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        assert "idx_url" in indexes
        assert "idx_crawled_at" in indexes
        
        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]
        assert journal_mode == "wal"
