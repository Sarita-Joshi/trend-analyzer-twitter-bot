# src/trendpulse_bot/ingestion/reddit_ingest.py

import requests
import json
from datetime import datetime, date
from pathlib import Path
from newspaper import Article
from src.schemas.article_schema import ArticleSchema  # adjust path as needed


class RedditIngestor:
    def __init__(self, run_id: str, subreddit="technology", limit=10, user_agent="TrendPulseBot/0.1"):
        self.run_id = run_id
        self.subreddit = subreddit
        self.limit = limit
        self.headers = {"User-Agent": user_agent}
        self.base_url = f"https://www.reddit.com/r/{self.subreddit}/hot.json?limit={self.limit}"
        self.articles = []

    def fetch(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        raw_data = response.json().get("data", {}).get("children", [])
        for post in raw_data:
            data = post["data"]
            title = data["title"]
            score = data["score"]
            reddit_url = f"https://www.reddit.com{data['permalink']}"
            external_url = data.get("url_overridden_by_dest", reddit_url)

            try:
                article = Article(external_url)
                article.download()
                article.parse()
                article.nlp()
                content = article.text.strip()
                summary = article.summary
                keywords = article.keywords
            except Exception as e:
                content = f"Error fetching content: {e}"
                summary = ""
                keywords = []

            self.articles.append(ArticleSchema(
                run_id=self.run_id,
                source="Reddit",
                source_domain=self.subreddit,
                url=reddit_url,
                resolved_url=external_url,
                title=title,
                content=content,
                summary=summary,
                keywords = keywords,
                published_at=datetime.utcfromtimestamp(data["created_utc"]).isoformat()
            ))

        return self.articles

    def filter_by_score(self, min_score=100):
        self.articles = [a for a in self.articles if isinstance(a.content, str) and not a.content.startswith("Error") and a.title and a.summary]
        return [a for a in self.articles if a.title and a.summary]

    def save_to_json(self, output_dir="data/raw"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filename = f"{output_dir}/reddit_{self.subreddit}_{date.today().isoformat()}.json"

        # Convert ArticleSchema objects to dicts
        articles_dict = [a.__dict__ for a in self.articles]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles_dict, f, indent=2)
        print(f"Saved {len(self.articles)} articles to {filename}")
        return filename


# Example usage
if __name__ == "__main__":
    ingestor = RedditIngestor(run_id="2024-06-18-reddit", subreddit="ArtificialInteligence", limit=10)
    ingestor.fetch()
    ingestor.filter_by_score(min_score=50)
    ingestor.save_to_json()
