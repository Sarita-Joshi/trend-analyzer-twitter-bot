# src/trendpulse_bot/ingestion/news_ingest.py

import requests
from datetime import datetime
import os

class NewsAPIIngestor:
    def __init__(self, api_key=None, query="AI", max_results=10):
        self.api_key = api_key or os.getenv("NEWS_API_KEY")
        self.query = query
        self.max_results = max_results
        self.url = "https://newsapi.org/v2/everything"

    def fetch_articles(self):
        params = {
            "q": self.query,
            "pageSize": self.max_results,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": self.api_key
        }

        response = requests.get(self.url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch NewsAPI data: {response.status_code}")

        data = response.json()
        articles = []
        for article in data.get("articles", []):
            articles.append({
                "title": article["title"],
                "description": article["description"],
                "source": article["source"]["name"],
                "url": article["url"],
                "published": article["publishedAt"]
            })

        return articles

# Example usage
if __name__ == "__main__":
    ingestor = NewsAPIIngestor(query="AI")
    results = ingestor.fetch_articles()
    for r in results:
        print(f"📰 {r['title']} ({r['source']})\n🔗 {r['url']}\n")
