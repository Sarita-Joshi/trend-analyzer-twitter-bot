from trendpulse_bot.ingestion.reddit_ingest import RedditIngestor
from trendpulse_bot.ingestion.twitter_ingest import TwitterIngestor
from trendpulse_bot.ingestion.hackernews_ingest import HackerNewsIngestor
from trendpulse_bot.ingestion.google_news_ingest import GoogleNewsIngestor
from trendpulse_bot.ingestion.newsapi_ingest import NewsAPIIngestor
from trendpulse_bot.db.db_manager import DBManager

from uuid import uuid4
from datetime import datetime

class TrendAggregator:
    def __init__(self, topic="AI"):

        self.run_id = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:6]}"

        self.topic = topic
        self.db = DBManager()
        self.collected = []

    def run_all_sources(self):
        print(f"🔍 Aggregating trends for topic: {self.topic}")

        # Reddit
        try:
            reddit = RedditIngestor(subreddit=self.topic, limit=10)
            items = reddit.fetch_posts()
            for item in items:
                self.db.insert_trend_item(self.topic, "reddit", item["title"], "", item["url"], item["score"])
                self.collected.append({
                    "source": "reddit", "title": item["title"], "url": item["url"], "score": item["score"]
                })
        except Exception as e:
            print(f"❌ Reddit error: {e}")

        # Twitter
        try:
            twitter = TwitterIngestor(query=self.topic, limit=15)
            df = twitter.fetch_tweets()
            for _, row in df.iterrows():
                self.db.insert_trend_item(self.topic, "twitter", row["tweet"], "", f"https://twitter.com/{row['username']}", 0)
                self.collected.append({
                    "source": "twitter", "title": row["tweet"], "url": f"https://twitter.com/{row['username']}"
                })
        except Exception as e:
            print(f"❌ Twitter error: {e}")

        # Hacker News
        try:
            hn = HackerNewsIngestor(limit=10)
            items = hn.fetch_top_stories()
            for item in items:
                self.db.insert_trend_item(self.topic, "hackernews", item["title"], "", item["url"], item["score"])
                self.collected.append({
                    "source": "hackernews", "title": item["title"], "url": item["url"], "score": item["score"]
                })
        except Exception as e:
            print(f"❌ Hacker News error: {e}")

        # Google News
        try:
            gn = GoogleNewsIngestor(query=self.topic, max_articles=10)
            items = gn.fetch_articles()
            for item in items:
                self.db.insert_trend_item(self.topic, "google_news", item["title"], item["summary"], item["link"])
                self.collected.append({
                    "source": "google_news", "title": item["title"], "content": item["summary"], "url": item["link"]
                })
        except Exception as e:
            print(f"❌ Google News error: {e}")

        # NewsAPI
        try:
            na = NewsAPIIngestor(query=self.topic, max_results=10)
            items = na.fetch_articles()
            for item in items:
                self.db.insert_trend_item(self.topic, "newsapi", item["title"], item["description"], item["url"])
                self.collected.append({
                    "source": "newsapi", "title": item["title"], "content": item["description"], "url": item["url"]
                })
        except Exception as e:
            print(f"❌ NewsAPI error: {e}")

        print(f"✅ Fetched and stored {len(self.collected)} trend items.")

    def get_aggregated_data(self):
        return self.collected  # For summarizer input

# Run from CLI
if __name__ == "__main__":
    agg = TrendAggregator(topic="Artificial Intelligence")
    agg.run_all_sources()
    data = agg.get_aggregated_data()
    print(f"\n🔢 Sample trend titles:\n" + "\n".join([d['title'] for d in data[:5]]))
