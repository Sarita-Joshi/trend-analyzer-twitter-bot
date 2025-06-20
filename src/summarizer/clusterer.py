from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

class SummaryClusterer:
    def __init__(self, n_clusters: int = None):
        self.n_clusters = n_clusters

    def _auto_select_k(self, embeddings, max_k=10):
        best_k = 2
        best_score = -1
        for k in range(2, min(max_k, len(embeddings))):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            if score > best_score:
                best_k = k
                best_score = score
        return best_k

    def cluster(self, summaries):
        embeddings = [item["embedding"] for item in summaries]
        embeddings_np = np.array(embeddings)

        if not self.n_clusters:
            self.n_clusters = self._auto_select_k(embeddings_np)

        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings_np)

        for i, item in enumerate(summaries):
            item["cluster_id"] = int(cluster_labels[i])

        return summaries



if __name__ == "__main__":

    from embedder import SummaryEmbedder

    embedder = SummaryEmbedder()
    embedded = embedder.embed_summaries("2024-06-17-01")

    clusterer = SummaryClusterer()  # auto-select k
    clustered = clusterer.cluster(embedded)

    for item in clustered[:3]:
        print(f"[Cluster {item['cluster_id']}] {item['title']}")
