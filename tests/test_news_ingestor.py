from src.ingestion.newsapi_ingest import NewsAPIIngestor

def test_newsapi_fetch(monkeypatch):
    def mock_fetch(*args, **kwargs):
        return [{'title': 'News Title', 'url': 'http://news.com', 'content': 'News content'}]
    
    monkeypatch.setattr(NewsAPIIngestor, 'fetch', mock_fetch)
    ni = NewsAPIIngestor("FAKE_KEY")
    data = ni.fetch("tech")
    assert len(data) > 0
    assert "title" in data[0]