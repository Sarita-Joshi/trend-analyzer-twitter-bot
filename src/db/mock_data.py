import sqlite3
import json
from datetime import datetime

# Setup
db_path = "data/trendpulse.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert dummy sources for cluster 1
sources = [
    {
        "run_id": "2024-06-17-01",
        "cluster_id": 1,
        "source_type": "news",
        "source_name": "The Verge",
        "url": "https://www.theverge.com/2024/06/17/ai-safety-warning",
        "title": "Experts raise alarm over AI safety risks",
        "content": "A growing number of researchers warn that current AI systems may pose unforeseen risks if not regulated effectively.",
        "fetched_at": datetime.utcnow()
    },
    {
        "run_id": "2024-06-17-01",
        "cluster_id": 1,
        "source_type": "reddit",
        "source_name": "r/technology",
        "url": "https://reddit.com/r/technology/ai_discussion",
        "title": "What scares you about AI?",
        "content": "A Reddit thread discussing various concerns from bias in algorithms to job displacement.",
        "fetched_at": datetime.utcnow()
    }
]

for source in sources:
    cursor.execute("""
        INSERT INTO articles (run_id, cluster_id, source, source_domain, url, title, content, fetched_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        source["run_id"],
        source["cluster_id"],
        source["source_type"],
        source["source_name"],
        source["url"],
        source["title"],
        source["content"],
        source["fetched_at"]
    ))


# Insert dummy poll
cursor.execute("""
    INSERT INTO polls (run_id, cluster_id, topic, question, options, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "2024-06-17-01",
    1,
    "AI Safety",
    "What concerns you most about AI?",
    json.dumps(["Job loss", "Bias", "Autonomy", "Nothing"]),
    datetime.utcnow()
))
poll_id = cursor.lastrowid

# Insert dummy results
options = [("Job loss", 48.2), ("Bias", 22.3), ("Autonomy", 17.8), ("Nothing", 11.7)]
for opt, pct in options:
    cursor.execute("""
        INSERT INTO poll_results (tweet_id, run_id, cluster_id, option_text, vote_percent, vote_total, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        poll_id,
        "2024-06-17-01",
        1,
        opt,
        pct,
        "2,341 votes",
        datetime.utcnow()
    ))

conn.commit()
conn.close()
print("✅ Sample poll and results inserted.")
