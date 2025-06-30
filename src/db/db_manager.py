import sqlite3
from dataclasses import asdict
from datetime import datetime
import json


class DBManager:
    def __init__(self, db_path="data/trendpulse.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

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
        self.conn.executemany(insert_query, values)
        self.conn.commit()

    def insert_summary_sentences(self, run_id, sentence_items: list):
        """
        sentence_items: list of dicts with keys:
        - article_id, sentence, cluster_id, cluster_label,
            distance_to_center, cluster_size, is_outlier
        """
        insert_query = """
        INSERT INTO summary_sentences (
            article_id, sentence, cluster_id, cluster_label,
            distance_to_center, cluster_size, is_outlier
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        values = [
            (
                item["article_id"],
                item["sentence"],
                item.get("cluster_id"),
                item.get("cluster_label"),
                float(item.get("distance_to_center", 0)),
                int(item.get("cluster_size", 0)),
                bool(item.get("is_outlier", False))
            )
            for item in sentence_items
        ]

        with self.conn:
            self.conn.executemany(insert_query, values)

    def insert_poll(self, run_id, poll_id, cluster_id, topic, question, options):
        self.cursor.execute("""
            INSERT INTO polls (id, run_id, cluster_id, topic, question, options)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            poll_id,
            run_id,
            cluster_id,
            topic,
            question,
            json.dumps(options),
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_poll_status(self, poll_id, status):
        self.cursor.execute("""
            UPDATE polls SET complete = ?
            WHERE poll_id = ?
        """, (status, poll_id))
        self.conn.commit()

    def insert_poll_result(self, poll_id, run_id, option_text, vote_percent, vote_total):
        self.cursor.execute("""
            INSERT INTO poll_results (poll_id, run_id, option_text, vote_percent, vote_total, scraped_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            poll_id,
            run_id,
            option_text,
            vote_percent,
            vote_total,
            datetime.utcnow()
        ))
        self.conn.commit()

    def close(self):
        self.conn.close()


# Optional quick test
if __name__ == "__main__":
    db = DBManager()
    print("Latest AI trends:")
    for row in db.get_trends_by_topic("AI"):
        print("-", row["title"])

    print("Topics stored:")
    print(db.count_trends_per_topic())
