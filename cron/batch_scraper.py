from scraper.poll_scraper import PollScraper
from db.db_manager import DBManager
import json

class BatchPollResultScraper:
    def __init__(self):
        self.db = DBManager()
        self.scraper = PollScraper()

    def get_all_poll_tweets(self):
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, run_id, cluster_id, question FROM polls")
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
        print(f"🔍 Found {len(tweets)} polls to scrape")

        for tweet in tweets:
            tweet_url = f"https://x.com/your_handle/status/{tweet['tweet_id']}"
            print(f"📊 Scraping poll → {tweet_url}")
            result = self.scraper.fetch_poll(tweet_url)

            if result:
                for opt in result["options"]:
                    *label_parts, percent_str = opt.split()
                    option_text = " ".join(label_parts)
                    try:
                        vote_percent = float(percent_str.strip('%'))
                    except ValueError:
                        vote_percent = None

                    self.db.insert_poll_result(
                        tweet_id=tweet["tweet_id"],
                        run_id=tweet["run_id"],
                        cluster_id=tweet["cluster_id"],
                        option_text=option_text,
                        vote_percent=vote_percent,
                        vote_total=result["votes"]
                    )
            else:
                print("⚠️ Skipped (poll not found or incomplete)")

        print("✅ Done scraping all polls.")
