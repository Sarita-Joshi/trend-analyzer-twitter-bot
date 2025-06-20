# src/trendpulse_bot/ingestion/google_news_ingest.py

import feedparser
from datetime import datetime

class GoogleNewsIngestor:
    def __init__(self, query="AI", max_articles=10):
        self.query = query
        self.feed_url = f"https://news.google.com/rss/search?q={query}"
        self.max_articles = max_articles

    def fetch_articles(self):
        feed = feedparser.parse(self.feed_url)
        articles = []
        for entry in feed.entries[:self.max_articles]:
            articles.append({
                "title": entry.title,
                "summary": entry.summary,
                "link": entry.link,
                "published": datetime(*entry.published_parsed[:6]).isoformat()
            })
        return articles

# Example
if __name__ == "__main__":
    ingestor = GoogleNewsIngestor("AI")
    articles = ingestor.fetch_articles()
    for art in articles:
        print(f"📰 {art['title']}\n🔗 {art['link']}\n")
