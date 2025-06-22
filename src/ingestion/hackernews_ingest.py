# src/trendpulse_bot/ingestion/hackernews_ingest.py

import requests
from newspaper import Article
from datetime import datetime

from src.schemas.article_schema import ArticleSchema

class HackerNewsIngestor:
    BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, run_id: str, limit: int = 10):
        self.limit = limit
        self.run_id = run_id

    def fetch(self):
        ids = requests.get(f"{self.BASE}/topstories.json").json()[:self.limit]
        stories = []

        for sid in ids:
            item = requests.get(f"{self.BASE}/item/{sid}.json").json()
            if not item:
                continue

            url = item.get("url", f"https://news.ycombinator.com/item?id={sid}")
            content = ""
            try:
                article = Article(url)
                article.download()
                article.parse()
                content = article.text.strip()
            except Exception as e:
                content = f"Error extracting content: {e}"

            story = ArticleSchema(
                run_id=self.run_id,
                source="Hacker News",
                url=url,
                resolved_url=url,
                title=item.get("title", ""),
                content=content,
                summary=None,
                published_at=datetime.fromtimestamp(item.get("time")).isoformat()
            )
            stories.append(story)

        return stories

# Example
if __name__ == "__main__":
    hn = HackerNewsIngestor(run_id="2024-06-17-hn", limit=2)
    articles = hn.fetch()
    for art in articles:
        print(f"📰 {art.title}\n📄 {art.url}\n✂️ {art.content[:150]}...\n")
