from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np
from collections import Counter

class SummaryClusterer:
    def __init__(self, n_clusters: int = None):
        self.n_clusters = n_clusters

    def _auto_select_k(self, embeddings, max_k=5):
        if len(embeddings) < 5:
            return 1  # Too few points to cluster meaningfully

        best_k = 2
        best_score = -1
        for k in range(2, min(max_k + 1, len(embeddings))):
            kmeans = KMeans(n_clusters=k, random_state=42)
            labels = kmeans.fit_predict(embeddings)
            try:
                # In _auto_select_k
                avg_dist = np.mean([np.linalg.norm(embeddings[i] - kmeans.cluster_centers_[labels[i]])
                                    for i in range(len(embeddings))])
                score = silhouette_score(embeddings, labels) - (0.1 * avg_dist)
                # score = silhouette_score(embeddings, labels)
            except Exception:
                continue
            if score > best_score:
                best_k = k
                best_score = score

        print(f"Best score: {best_score}")
        # if best_score < 0.2:  # Weak separation, fallback to 1 cluster
        #     return 1

        return best_k

    def cluster(self, embeddings):
        # embeddings_np = np.array(embeddings)
        from sklearn.preprocessing import normalize
        embeddings_np = normalize(embeddings)


        if not self.n_clusters:
            self.n_clusters = self._auto_select_k(embeddings_np)
        print(f"Created {self.n_clusters} clusters.")
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(embeddings_np)
        distances = kmeans.transform(embeddings_np)

        cluster_counts = Counter(cluster_labels)

        # Compute threshold for outliers based on Z-score distance per cluster
        cluster_thresholds = {}
        for cluster_id in range(self.n_clusters):
            cluster_distances = [distances[i][cluster_id] for i in range(len(embeddings)) if cluster_labels[i] == cluster_id]
            if len(cluster_distances) > 1:
                mean = np.mean(cluster_distances)
                std = np.std(cluster_distances)
                cluster_thresholds[cluster_id] = mean + 1.5 * std  # z-score threshold
            else:
                cluster_thresholds[cluster_id] = float('inf')  # Never mark singletons here (already handled below)
        
        cluster_data = []
        for i in range(len(embeddings)):
            item = {}
            cid = cluster_labels[i]
            dist = distances[i][cid]
            item["cluster_id"] = int(cid)
            item["distance_to_center"] = dist
            item["cluster_size"] = cluster_counts[cid]

            # Outlier if (a) small cluster or (b) too far from center
            is_small_cluster = cluster_counts[cid] <= 1 and self.n_clusters > 1
            is_far = dist > cluster_thresholds[cid]
            item["is_outlier"] = is_small_cluster or is_far
            cluster_data.append(item)

        return cluster_data
    
    def filter_outliers(self, summaries):
        return [item for item in summaries if not item.get("is_outlier", False)]


if __name__ == "__main__":

    from embedder import SummaryEmbedder

    embedder = SummaryEmbedder()
    embedded = embedder.embed_summaries("2024-06-17-01")

    clusterer = SummaryClusterer()  # auto-select k
    clustered = clusterer.cluster(embedded)
    filtered = clusterer.filter_outliers(clustered)

    for item in filtered[:3]:
        print(f"[Cluster {item['cluster_id']}] {item['title']} (Outlier: {item['is_outlier']})")
