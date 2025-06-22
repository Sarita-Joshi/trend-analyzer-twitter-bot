from ingestion.trend_aggregator import TrendAggregator
from db.db_manager import DBManager 
from poller import PollGenerator, PollPoster, PollScraper
from summarizer import Summarizer
from datetime import datetime
import traceback

def run_pipeline(topic="AI"):
    db = DBManager()
    run_id = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    started_at = datetime.utcnow().isoformat()

    try:
        # db.insert_run(run_id, topic, started_at)
        print(f"🟡 Run started: {run_id} for topic: {topic}")

        aggregator = TrendAggregator(run_id, topic)
        articles = aggregator.run_all_sources()
        # db.insert_articles_bulk(articles, run_id)

        summarizer = Summarizer()
        summerized_data = summarizer.summarize(articles=articles)

        cluster_summary = summarizer.get_condensed_summary(summerized_data)
        
        # db.update_summaries_bulk(articles, run_id)

        # Poll creation
        poll_creator = PollGenerator(topic=topic)
        poll = poll_creator.generate_poll(cluster_summary['summary'])
        poll_id = db.insert_poll(run_id, cluster_summary['cluster_id'], topic, poll['question'], poll['options'])
        
        db.update_poll_status(run_id, poll_id=poll_id, poll_status="active")
        db.update_run_status(run_id, "success")
        
        print(f"✅ Pipeline completed and poll posted with ID: {poll_id}")

    except Exception as e:
        db.update_run_status(run_id, "failed", ended_at=datetime.utcnow().isoformat())
        db.update_poll_status(run_id, poll_status="error")
        print("❌ Pipeline failed:", str(e))
        traceback.print_exc()
