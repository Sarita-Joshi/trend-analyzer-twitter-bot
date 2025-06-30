from src.poller.poll_scraper import PollScraper
from src.db.db_manager import DBManager
import os
from dotenv import load_dotenv

load_dotenv()

class BatchPollResultScraper:
    def __init__(self):
        self.db = DBManager()
        self.scraper = PollScraper()

    def get_all_poll_tweets(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, run_id, cluster_id, question FROM polls where complete=0")
        rows = cursor.fetchall()
        return [
            {
                "tweet_id": row[0],
                "run_id": row[1],
                "cluster_id": row[2],
                "question": row[3]
            }
            for row in rows
        ]

    def scrape_and_store_all(self):
        tweets = self.get_all_poll_tweets()
        print(f"Found {len(tweets)} polls to scrape")

        for tweet in tweets:
            tweet_url = f"https://x.com/{os.getenv('X_USERNAME')}/status/{tweet['tweet_id']}"
            print(f"📊 Scraping poll → {tweet_url}")
            result = self.scraper.fetch_poll(tweet_url)
            print(result)
            if result:
                self.scraper.save_poll_result(tweet['tweet_id'], tweet['run_id'], result)
            else:
                print("Skipped (poll not found or incomplete)")

        print("Done scraping all polls.")


if __name__ == '__main__':
    obj = BatchPollResultScraper()
    obj.scrape_and_store_all()