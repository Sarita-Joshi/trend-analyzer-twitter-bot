import sqlite3
import pytest
from src.db.db_manager import DBManager

@pytest.fixture
def db():
    return DBManager("test_trendpulse.db")

def test_create_tables(db):
    db.create_tables()
    cursor = db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    assert 'articles' in tables

def test_insert_article(db):
    article = {
        'run_id': 'run_test',
        'source': 'reddit',
        'title': 'Test title',
        'url': 'http://test.com',
        'content': 'This is test content',
        'published_at': '2024-01-01',
        'summary': '',
        'cluster_id': 1,
        'cluster_label': 'test'
    }
    db.insert_article(article)
    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM articles WHERE title='Test title'")
    result = cursor.fetchone()
    assert result is not None