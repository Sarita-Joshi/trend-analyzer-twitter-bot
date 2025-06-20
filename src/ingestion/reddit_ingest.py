# src/trendpulse_bot/ingestion/reddit_ingest.py

import requests
import json
from datetime import datetime, date
from pathlib import Path

class RedditIngestor:
    def __init__(self, subreddit="technology", limit=10, user_agent="TrendPulseBot/0.1"):
        self.subreddit = subreddit
        self.limit = limit
        self.headers = {"User-Agent": user_agent}
        self.base_url = f"https://www.reddit.com/r/{self.subreddit}/hot.json?limit={self.limit}"
        self.posts = []

    def fetch_posts(self):
        response = requests.get(self.base_url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        raw_data = response.json().get("data", {}).get("children", [])
        self.posts = [
            {
                "title": post["data"]["title"],
                "score": post["data"]["score"],
                "url": f"https://www.reddit.com{post['data']['permalink']}",
                "created_utc": datetime.utcfromtimestamp(post["data"]["created_utc"]).isoformat()
            }
            for post in raw_data
        ]
        return self.posts

    def filter_by_score(self, min_score=100):
        self.posts = [p for p in self.posts if p["score"] >= min_score]
        return self.posts

    def save_to_json(self, output_dir="data/raw"):
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        filename = f"{output_dir}/reddit_{self.subreddit}_{date.today().isoformat()}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.posts, f, indent=2)
        print(f"✅ Saved {len(self.posts)} posts to {filename}")
        return filename

# Example usage
if __name__ == "__main__":
    ingestor = RedditIngestor(subreddit="ArtificialIntelligence", limit=15)
    ingestor.fetch_posts()
    ingestor.filter_by_score(min_score=50)
    ingestor.save_to_json()
