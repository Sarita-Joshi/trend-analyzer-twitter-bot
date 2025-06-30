from src.ingestion.trend_aggregator import TrendAggregator
from src.db.db_manager import DBManager 
from src.poller import PollGenerator, PollPoster, PollScraper
from src.summarizer import Summarizer
from datetime import datetime
import traceback

def run_pipeline(topic="AI"):
    db = DBManager()
    run_id = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.utcnow().isoformat()

    try:
        db.insert_run(run_id, topic, started_at)
        print(f"🟡 Run started: {run_id} for topic: {topic}")

        aggregator = TrendAggregator(run_id, topic)
        articles = aggregator.run_all_sources()
        db.insert_trend_items(articles)

        summarizer = Summarizer()
        summerized_data = summarizer.summarize(articles=articles)

        cluster_summary = summarizer.get_condensed_summary(summerized_data)
        
        db.insert_summary_sentences(run_id, summerized_data)

        # Poll creation
        poll_creator = PollGenerator(topic=topic)
        poll = poll_creator.generate_poll(cluster_summary['summary'])

        tweet_id = PollPoster().post_poll(
            question=poll['question'],
            options=poll['options'][:4],
            duration_minutes=1440
        )

        #TODO-Update poll details in  dbtables
        db.insert_poll(run_id, tweet_id, cluster_summary['cluster_id'], topic, poll['question'], poll['options'])
        db.update_run_status(run_id, "success")

        print(poll)
        print(f"Pipeline completed and poll posted with ID: {tweet_id}")

    except Exception as e:
        db.update_run_status(run_id, "failed", ended_at=datetime.utcnow().isoformat())
        print("Pipeline failed:", str(e))
        traceback.print_exc()


if __name__ == "__main__":
    run_pipeline('wallstreet')