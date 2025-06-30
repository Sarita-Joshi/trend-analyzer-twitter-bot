# src/trendpulse_bot/ingestion/news_ingest.py

import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from newspaper import Article
from src.schemas.article_schema import ArticleSchema  # Adjust path if needed

load_dotenv()

class NewsAPIIngestor:
    def __init__(self, run_id: str, api_key=None, query="AI", max_results=10):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.query = query
        self.max_results = max_results
        self.run_id = run_id
        self.url = "https://newsapi.org/v2/top-headlines"

    def fetch(self):
        params = {
            "apiKey": self.api_key,
            "country": "us",
            "q": self.query,
            "pageSize": self.max_results,
            "sortBy": "publishedAt",
        }

        response = requests.get(self.url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch NewsAPI data: {response.status_code}")

        data = response.json()
        articles = []

        for article in data.get("articles", []):
            url = article["url"]
            try:
                a = Article(url)
                a.download()
                a.parse()
                a.nlp()
                content = a.text.strip()
                summary = a.summary
                keywords = a.keywords
            except Exception as e:
                content = f"Error fetching content: {e}"
                summary = article.get("description", "")
                keywords = []

            articles.append(ArticleSchema(
                run_id=self.run_id,
                source="News API",
                source_domain=article["source"]["name"],
                url=url,
                resolved_url=url,
                title=article["title"],
                content=content,
                summary=summary,
                keywords=keywords,
                published_at=article["publishedAt"],
            ))

        return articles


# Example usage
if __name__ == "__main__":
    ingestor = NewsAPIIngestor(run_id="2024-06-18-ai-news", query="AI")
    results = ingestor.fetch()
    for r in results:
        print(f"📰 {r.title} ({r.source})\n🔗 {r.url}\n✂️ {r.content[:100]}...\n")
