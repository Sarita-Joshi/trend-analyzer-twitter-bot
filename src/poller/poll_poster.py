import os
import json
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

load_dotenv()

class PollPoster:
    def __init__(self):
        self.auth = OAuth1(
            os.getenv("X_API_KEY"),
            os.getenv("X_API_SECRET"),
            os.getenv("X_ACCESS_TOKEN"),
            os.getenv("X_ACCESS_TOKEN_SECRET")
        )

    def post_poll(self, question, options, duration_minutes=1440):
        """
        Posts a poll with 2-4 options.
        """
        payload = {
            "text": question,
            "poll": { "duration_minutes": duration_minutes, "options": options,},
        }
        try:
            response = requests.post(
                url="https://api.twitter.com/2/tweets",
                auth=self.auth,
                json=payload
            )

            if response.status_code != 201:
                raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )

            print("Response code: {}".format(response.status_code))
            json_response = response.json()
            print(json.dumps(json_response, indent=4, sort_keys=True))
            return json_response['data']['id']
        except Exception as e:
            print("Failed to post poll:", str(e))
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
