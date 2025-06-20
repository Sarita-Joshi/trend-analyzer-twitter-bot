from sentence_transformers import SentenceTransformer
from db.db_manager import DBManager

class SummaryEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.db = DBManager()

    def get_summaries(self, run_id: str):
        """
        Returns: List of dicts: {id, summary, title, source}
        """
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT id, summary_text, title, source
            FROM articles
            WHERE run_id = ? AND summary_text IS NOT NULL
        """, (run_id,))
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "summary": row[1],
                "title": row[2],
                "source": row[3]
            }
            for row in rows
        ]

    def embed_summaries(self, run_id: str):
        summaries = self.get_summaries(run_id)
        texts = [s["summary"] for s in summaries]
        embeddings = self.model.encode(texts)

        for i, embed in enumerate(embeddings):
            summaries[i]["embedding"] = embed

        return summaries


if __name__ == "__main__":

    embedder = SummaryEmbedder()
    embedded_summaries = embedder.embed_summaries("2024-06-17-01")

    print(f"Found {len(embedded_summaries)} embeddings:")
    print(embedded_summaries[0].keys())  # should include 'embedding'
