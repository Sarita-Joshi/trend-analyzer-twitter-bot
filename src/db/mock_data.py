from db_manager import DBManager
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid
import random
import sqlite3
# Mock Article Schema as a dataclass
@dataclass
class Article:
    run_id: str
    source: str
    source_domain: str
    url: str
    resolved_url: str
    title: str
    content: str
    published_at: str
    summary: str
    keywords: list
    author: str
    cluster_id: int
    cluster_label: str

# Initialize DB
db = DBManager("data/test_trendpulse.db")
run_id = f"testrun_{uuid.uuid4().hex[:8]}"
topic = "Test Topic"

def setup():
    db_path = "data/test_trendpulse.db"
    schema_path = "src/db/schema.sql"

    conn = sqlite3.connect(db_path)
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    print("Database initialized using schema.sql")

setup()

# 1. Insert a run
db.insert_run(run_id, topic, started_at=datetime.utcnow().isoformat())
print("✅ Inserted run.")

# 2. Insert articles
articles = []
for i in range(3):
    articles.append(Article(
        run_id=run_id,
        source="Test Source",
        source_domain="testsource.com",
        url=f"https://example.com/article{i}",
        resolved_url=f"https://example.com/resolved/article{i}",
        title=f"Test Article {i}",
        content="This is the content of the test article.",
        published_at=datetime.utcnow().isoformat(),
        summary="This is a summary.",
        keywords=["test", "mock", "data"],
        author="Author X",
        cluster_id=random.randint(0, 1),
        cluster_label="Test Cluster"
    ))
db.insert_trend_items(articles)
print("✅ Inserted test articles.")

# 3. Update run status
db.update_run_status(run_id, "success")
print("✅ Updated run status.")

# 4. Insert poll
poll_id = db.insert_poll(
    run_id=run_id,
    cluster_id=0,
    topic=topic,
    question="What do you think?",
    options=["Option A", "Option B", "Option C"]
)
print(f"✅ Inserted poll with ID {poll_id}.")

# 5. Update poll status
db.update_poll_status(run_id, poll_id=poll_id, poll_status="active")
print("✅ Updated poll status.")

# 6. Insert poll results
db.insert_poll_result(
    tweet_id=str(poll_id),
    run_id=run_id,
    cluster_id=0,
    option_text="Option A",
    vote_percent=60.0,
    vote_total="120"
)
print("✅ Inserted poll result.")

# 7. Fetch data
print("\n🧪 Fetching data to validate:")
print("- Trends by topic:", db.get_trends_by_topic(topic))
print("- Recent trends:", db.get_recent_trends())
print("- Sources used:", db.get_sources_used())
print("- Trends per topic:", db.count_trends_per_topic())
print("- Articles for run:", db.fetch_articles_by_run_id(run_id))

# 8. Cleanup
db.close()
