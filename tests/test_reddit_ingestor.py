from src.ingestion.reddit_ingest import RedditIngestor

def test_reddit_ingestor_fetch(monkeypatch):
    def mock_fetch(*args, **kwargs):
        return [{'title': 'Reddit News', 'content': 'Content from reddit', 'url': 'http://reddit.com'}]

    monkeypatch.setattr(RedditIngestor, 'fetch_posts', mock_fetch)
    ri = RedditIngestor()
    results = ri.fetch("AI", limit=2)
    assert isinstance(results, list)
    assert 'title' in results[0]