import tweepy
import os
from dotenv import load_dotenv
import time

load_dotenv()

class PollPoster:
    def __init__(self):
        self.client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
        )

    def post_poll(self, question, options, duration_minutes=1440):
        """
        Posts a poll with 2–4 options.
        """
        if not (2 <= len(options) <= 4):
            raise ValueError("Twitter/X allows only 2 to 4 poll options")

        try:
            response = self.client.create_tweet(
                text=question,
                poll_options=options,
                poll_duration_minutes=duration_minutes
            )
            tweet_id = response.data['id']
            print(f"✅ Poll posted: https://x.com/user/status/{tweet_id}")
            return tweet_id
        except Exception as e:
            print("❌ Failed to post poll:", str(e))
            return None



if __name__ == "__main__":

    poster = PollPoster()

    poster.post_poll(
        question="What should be prioritized in the new EV policy?",
        options=[
            "Subsidy reform",
            "Charging infra",
            "Tax exemption"
        ],
        duration_minutes=60  # 1 hour
    )
