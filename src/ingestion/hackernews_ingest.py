# src/trendpulse_bot/ingestion/hackernews_ingest.py

import requests

class HackerNewsIngestor:
    BASE = "https://hacker-news.firebaseio.com/v0"

    def __init__(self, limit=10):
        self.limit = limit

    def fetch_top_stories(self):
        ids = requests.get(f"{self.BASE}/topstories.json").json()[:self.limit]
        stories = []

        for sid in ids:
            item = requests.get(f"{self.BASE}/item/{sid}.json").json()
            if item:
                stories.append({
                    "title": item.get("title"),
                    "score": item.get("score"),
                    "url": item.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    "time": item.get("time")
                })
        return stories

# Example
if __name__ == "__main__":
    hn = HackerNewsIngestor(5)
    for story in hn.fetch_top_stories():
        print(f"🚀 {story['title']} ({story['score']} points)")
        print(f"🔗 {story['url']}\n")
