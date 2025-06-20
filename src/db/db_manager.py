import sqlite3
from datetime import datetime
from pathlib import Path
import json

class DBManager:
    def __init__(self, db_path="data/trendpulse.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # for dict-like rows
        self.create_tables()


    def insert_trend_item(self, run_id, topic, source, title, content, url, score=None):
        self.conn.execute('''
        INSERT INTO aggregated_trends (run_id, topic, source, title, content, url, score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (run_id, topic, source, title, content, url, score or 0, datetime.utcnow().isoformat()))
        self.conn.commit()

    def get_trends_by_topic(self, topic, limit=20):
        rows = self.conn.execute('''
            SELECT * FROM aggregated_trends
            WHERE topic = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (topic, limit)).fetchall()
        return [dict(row) for row in rows]

    def get_recent_trends(self, limit=50):
        rows = self.conn.execute('''
            SELECT * FROM aggregated_trends
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,)).fetchall()
        return [dict(row) for row in rows]

    def get_sources_used(self):
        rows = self.conn.execute('''
            SELECT DISTINCT source FROM aggregated_trends
        ''').fetchall()
        return [row["source"] for row in rows]

    def count_trends_per_topic(self):
        rows = self.conn.execute('''
            SELECT topic, COUNT(*) as count FROM aggregated_trends
            GROUP BY topic
        ''').fetchall()
        return [{ "topic": row["topic"], "count": row["count"] } for row in rows]

    def fetch_articles_by_run_id(self, run_id: str):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, text FROM articles WHERE run_id = ?", (run_id,))
        rows = cursor.fetchall()
        return [{"id": row[0], "text": row[1]} for row in rows]

    def update_summary(self, article_id: int, summary: str):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE articles SET summary_text = ? WHERE id = ?", (summary, article_id))
        self.conn.commit()

    def insert_poll(self, run_id, cluster_id, topic, question, options):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO polls (run_id, cluster_id, topic, question, options, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            cluster_id,
            topic,
            question,
            json.dumps(options),
            datetime.now()
        ))
        self.conn.commit()

    from datetime import datetime

    def insert_poll_result(self, tweet_id, run_id, cluster_id, option_text, vote_percent, vote_total):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO poll_results (tweet_id, run_id, cluster_id, option_text, vote_percent, vote_total, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            tweet_id,
            run_id,
            cluster_id,
            option_text,
            vote_percent,
            vote_total,
            datetime.utcnow()
        ))
        self.conn.commit()

    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = DBManager()
    print("🧵 Latest AI trends:")
    for row in db.get_trends_by_topic("AI"):
        print("-", row["title"])

    print("\n📚 Topics stored:")
    print(db.count_trends_per_topic())
