from sentence_transformers import SentenceTransformer
from src.db.db_manager import DBManager

class SummaryEmbedder:
    def __init__(self, model_name: str = "all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)
        self.db = DBManager()


    def embed_summaries(self, texts):
        embeddings = self.model.encode(texts)
        return embeddings


if __name__ == "__main__":

    embedder = SummaryEmbedder()
    embedded_summaries = embedder.embed_summaries("2024-06-17-01")

    print(f"Found {len(embedded_summaries)} embeddings:")
    print(embedded_summaries[0].keys())  # should include 'embedding'
