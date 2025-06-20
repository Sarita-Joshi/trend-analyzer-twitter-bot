# src/trendpulse_bot/ingestion/twitter_ingest.py

import twint
import pandas as pd
from datetime import date
from pathlib import Path

class TwitterIngestor:
    def __init__(self, query="AI", limit=50, lang="en", output_dir="data/raw"):
        self.query = query
        self.limit = limit
        self.lang = lang
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.df = pd.DataFrame()

    def fetch_tweets(self):
        config = twint.Config()
        config.Search = self.query
        config.Limit = self.limit
        config.Lang = self.lang
        config.Hide_output = True
        config.Pandas = True

        twint.run.Search(config)
        self.df = twint.output.panda.Tweets_df

        return self.df[["date", "username", "tweet"]].copy()

    def save_to_csv(self):
        if self.df.empty:
            print("⚠️ No data to save. Run fetch_tweets() first.")
            return

        filename = self.output_dir / f"twitter_{self.query}_{date.today().isoformat()}.csv"
        self.df.to_csv(filename, index=False)
        print(f"✅ Saved {len(self.df)} tweets to {filename}")
        return filename

# Example usage
if __name__ == "__main__":
    ingestor = TwitterIngestor(query="AI", limit=30)
    tweets = ingestor.fetch_tweets()
    print(tweets.head())
    ingestor.save_to_csv()
