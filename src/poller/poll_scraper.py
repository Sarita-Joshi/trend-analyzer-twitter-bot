import requests
from bs4 import BeautifulSoup
import re

from src.db.db_manager import DBManager

class PollScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }
        self.db = DBManager()

    def fetch_poll(self, tweet_url):
        try:
            res = requests.get(tweet_url, headers=self.headers)
            if res.status_code != 200:
                print(f"Failed to fetch tweet page: {res.status_code}")
                return None

            soup = BeautifulSoup(res.text, "html.parser")

            # Poll options are embedded in spans with %
            options = []
            for span in soup.find_all("span", string=re.compile(r"\d{1,3}\.\d%")):
                text = span.get_text(strip=True)
                percent_match = re.search(r"(\d{1,3}\.\d)%", text)
                if percent_match:
                    options.append(text)

            # Try to extract vote count
            votes_tag = soup.find("span", string=re.compile(r"votes"))
            votes = votes_tag.get_text(strip=True) if votes_tag else "Unknown"

            return {
                "options": options,
                "votes": votes
            }

        except Exception as e:
            print("Exception while scraping poll:", e)
            return None

    def save_poll_result(self, result):

        if result:
            for opt in result["options"]:
                # Parse "Option A 52.3%" → split text & percent
                *label_parts, percent_str = opt.split()
                option_text = " ".join(label_parts)
                percent = float(percent_str.strip('%'))
                self.db.insert_poll_result(
                    tweet_id=tweet_id,
                    run_id=run_id,
                    cluster_id=cluster_id,
                    option_text=option_text,
                    vote_percent=percent,
                    vote_total=result["votes"]
                )

if __name__ == "__main__":

    scraper = PollScraper()

    tweet_url = "https://x.com/your_handle/status/1234567890123456789"
    result = scraper.fetch_poll(tweet_url)

    print(result)
    # Output:
    # {
    #   "options": ["Option A 53.2%", "Option B 46.8%"],
    #   "votes": "1,234 votes"
    # }
