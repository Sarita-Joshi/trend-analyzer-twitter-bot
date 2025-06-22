from .extractive import ExtractiveSummarizer
from .embedder import SummaryEmbedder 
from .clusterer import SummaryClusterer
from .labeler import ClusterLabeler

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class Summarizer:
    def __init__(self):
        self.extractor = ExtractiveSummarizer()
        self.embedder = SummaryEmbedder()
        self.clusterer = SummaryClusterer()
        self.labeler = ClusterLabeler()


    def summarize(self, articles):
        # Step 1: Extract summaries
        summaries = self.extractor.summarize_articles(articles)

        # Step 2: Split into sentences
        sentence_data = []
        for i, item in enumerate(summaries):
            for sentence in sent_tokenize(item["summary"]):
                if sentence.strip():
                    sentence_data.append({
                        "sentence": sentence.strip(),
                        "article_id": item['id']
                    })

        # Step 3: Embed
        embeddings = self.embedder.embed_summaries([s["sentence"] for s in sentence_data])
    
        # Step 4: Cluster
        cluster_data = self.clusterer.cluster(sentence_data)

        final_lst = []
        for sent, clu in zip(sentence_data,cluster_data):
            sent.update(clu)

        # Step 5: Filter or label if needed
        labeled = self.labeler.label_clusters(sentence_data)

        return labeled
    
    def get_condensed_summary(self, sentence_data, char_limit=2048):
        """
        Selects the most dense cluster and returns its top sentences within a character limit.
        """
        from collections import defaultdict

        # Group by cluster
        cluster_distances = defaultdict(list)
        cluster_sentences = defaultdict(list)

        for item in sentence_data:
            if not item.get("is_outlier", False):
                cid = item["cluster_id"]
                cluster_distances[cid].append(item["distance_to_center"])
                cluster_sentences[cid].append(item)

        # Compute average distance for each cluster
        avg_distance = {
            cid: sum(distances) / len(distances)
            for cid, distances in cluster_distances.items()
        }

        # Select most dense cluster (lowest avg distance)
        most_dense_cluster_id = min(avg_distance, key=avg_distance.get)

        # Sort sentences in that cluster by proximity to center
        top_sentences = sorted(
            cluster_sentences[most_dense_cluster_id],
            key=lambda x: x["distance_to_center"]
        )

        # Select top sentences within char_limit
        selected = []
        total_chars = 0
        for s in top_sentences:
            sentence = s["sentence"].strip()
            if total_chars + len(sentence) <= char_limit:
                selected.append(sentence)
                total_chars += len(sentence)
            else:
                break

        return {
            "cluster_id": most_dense_cluster_id,
            "cluster_label": top_sentences[0].get("cluster_label", f"Cluster {most_dense_cluster_id}"),
            "summary": selected
        }



__all__ = [
    Summarizer
]