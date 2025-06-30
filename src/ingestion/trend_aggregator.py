from .reddit_ingest import RedditIngestor
from .twitter_ingest import TwitterIngestor
from .hackernews_ingest import HackerNewsIngestor
from .google_news_ingest import GoogleNewsIngestor
from .newsapi_ingest import NewsAPIIngestor
from src.schemas.article_schema import ArticleSchema

from uuid import uuid4
from datetime import datetime

SAMPLE_CONFIG = {
    'reddit': True,
    'x': False,
    'google-news': True,
    'hacker-news': True,
    'news-api': True, #Temp - not to use api credits until testing
}

class TrendAggregator:
    def __init__(self, run_id, topic="AI", config=None):
        self.run_id = run_id
        self.topic = topic
        self.config = config or SAMPLE_CONFIG

        self.collected = []

    def run_all_sources(self):
        print(f"Aggregating trends for topic: {self.topic}")

        # Reddit
        try:
            if self.config.get('reddit'):
                reddit = RedditIngestor(run_id=self.run_id, subreddit=self.topic, limit=5)
                items = reddit.fetch()
                self.collected.extend(items)
                print('Collected posts from Reddit.')
        except Exception as e:
            print(f"Reddit error: {e}")

        # Twitter (skip for now)
        try:
            if self.config.get('x'):
                print("Not Implemented yet.")
        except Exception as e:
            print(f"Twitter error: {e}")

        # Hacker News
        try:
            if self.config.get('hacker-news'):
                hn = HackerNewsIngestor(run_id=self.run_id, limit=5)
                items = hn.fetch()
                self.collected.extend(items)
                print('Collected stories from HackerNews.')
        except Exception as e:
            print(f"Hacker News error: {e}")

        # Google News
        try:
            if self.config.get('google-news'):
                gn = GoogleNewsIngestor(run_id=self.run_id, query=self.topic, max_articles=5)
                items = gn.fetch()
                self.collected.extend(items)
                print('Collected articles from Google News.')
        except Exception as e:
            print(f"Google News error: {e}")

        # NewsAPI
        try:
            if self.config.get('news-api'):
                na = NewsAPIIngestor(run_id=self.run_id, query=self.topic, max_results=5)
                items = na.fetch()
                self.collected.extend(items)
                print('Collected articles from NewsAPI.')
        except Exception as e:
            print(f"NewsAPI error: {e}")

        print(f"Fetched and stored {len(self.collected)} trend items.")

        return self.collected

    def get_aggregated_data(self):
        return self.collected

if __name__ == "__main__":
    agg = TrendAggregator(topic="ArtificialInteligence")
    agg.run_all_sources()
    data = agg.get_aggregated_data()
    print(f"\\n🔢 Sample trend titles:\\n" + "\\n".join([d.title for d in data[:5]]))
