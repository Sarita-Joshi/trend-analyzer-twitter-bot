import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
import json

class DBManager:
    def __init__(self, db_path="data/trendpulse.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # for dict-like rows
        # self.create_tables()

    def insert_run(self, run_id, topic, started_at):
        self.cursor.execute("""
            INSERT INTO runs (run_id, topic, started_at, status)
            VALUES (?, ?, ?, 'started')
        """, (run_id, topic, started_at))
        self.conn.commit()

    def update_run_status(self, run_id, status, ended_at=None):
        self.cursor.execute("""
            UPDATE runs SET status = ?, ended_at = ?
            WHERE run_id = ?
        """, (status, ended_at or datetime.utcnow().isoformat(), run_id))
        self.conn.commit()

    def update_poll_status(self, run_id, poll_id=None, poll_status=None):
        updates = []
        params = []
        if poll_id:
            updates.append("poll_id = ?")
            params.append(poll_id)
        if poll_status:
            updates.append("poll_status = ?")
            params.append(poll_status)

        query = f"UPDATE runs SET {', '.join(updates)} WHERE run_id = ?"
        params.append(run_id)

        self.cursor.execute(query, tuple(params))
        self.conn.commit()

    def insert_trend_items(self, articles):
        values = []
        for article in articles:
            a = asdict(article)
            values.append((
                a["run_id"],
                a["source"],
                a.get("source_domain"),
                a.get("url"),
                a.get("resolved_url"),
                a["title"],
                a["content"],
                a.get("published_at"),
                a.get("summary"),
                ",".join(a.get("keywords", [])) if a.get("keywords") else None,
                a.get("author"),
                a.get("cluster_id"),
                a.get("cluster_label")
            ))


        insert_query = """
        INSERT INTO articles (
            run_id, source, source_domain, url, resolved_url, title,
            content, published_at, summary, keywords, author,
            cluster_id, cluster_label
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        with self.conn:
            self.conn.executemany(insert_query, values)
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
        return cursor.lastrowid

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
