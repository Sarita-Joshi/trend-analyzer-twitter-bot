from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

from src.db.db_manager import DBManager

class PollScraper:
    def __init__(self):
        self.db = DBManager()

    def get_page_source(self, tweet_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(tweet_url)

        time.sleep(5)
        page_source = driver.page_source
        driver.quit()

        return page_source

    def fetch_poll(self, tweet_url):
        page_source = self.get_page_source(tweet_url)
        soup = BeautifulSoup(page_source, 'html.parser')
        tweet = soup.find('div', {'data-testid': 'tweetText'})
        if not tweet:
            return None

        poll_div = soup.find('div', {'data-testid': 'cardPoll'})
        options = []
        for li in poll_div.find_all('li', {'role': 'listitem'}):
            option_text = li.find_all('span', recursive=True)[1].get_text(strip=True)
            percent_text = li.find_all('span', recursive=True)[-1].get_text(strip=True)
            options.append((option_text, percent_text))

        total_votes = None
        for span in poll_div.find_all('span'):
            if 'votes' in span.get_text():
                total_votes = span.get_text(strip=True)
                break
        
        return {
            "poll": tweet.get_text(),
            "options": options,
            "votes": total_votes
        }


    def save_poll_result(self, tweeet_id, run_id, result):

        if result:
            for opt in result["options"]:
                # Parse "Option A 52.3%" → split text & percent
                *label_parts, percent_str = opt.split()
                option_text = " ".join(label_parts)
                percent = float(percent_str.strip('%'))
                self.db.insert_poll_result(
                    tweet_id=tweet_id,
                    run_id=run_id,
                    option_text=option_text,
                    vote_percent=percent,
                    vote_total=result["votes"]
                )
                
                self.db.update_poll_status(run_id,tweet_id, "Complete")

if __name__ == "__main__":

    scraper = PollScraper()
    tweet_id = "1936706311997317549"
    tweet_url = "https://x.com/trendpulse325/status/" + tweet_id
    result = scraper.fetch_poll(tweet_url)

    print(result)
    # Output:
    # {
    #   "options": ["Option A 53.2%", "Option B 46.8%"],
    #   "votes": "1,234 votes"
    # }
