from collections import Counter, defaultdict
import re

import nltk
from nltk.corpus import stopwords
from collections import Counter
import string

# Ensure you have the stopwords downloaded
nltk.download('stopwords')
STOP_WORDS = set(stopwords.words('english'))


class ClusterLabeler:
    def __init__(self, stopwords=None):
        self.stopwords = set(STOP_WORDS) 

    def extract_keywords(self, text, top_n=3):
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [w for w in words if w not in self.stopwords and len(w) > 3]
        return Counter(keywords).most_common(top_n)

    def label_clusters(self, clustered_summaries):
        cluster_map = defaultdict(list)
        for item in clustered_summaries:
            cluster_map[item["cluster_id"]].append(item["sentence"])

        cluster_labels = {}
        for cluster_id, summaries in cluster_map.items():
            full_text = " ".join(summaries)
            keywords = self.extract_keywords(full_text)
            label = ", ".join([kw for kw, _ in keywords])
            cluster_labels[cluster_id] = label

        # Attach cluster label to each summary
        for item in clustered_summaries:
            item["cluster_label"] = cluster_labels[item["cluster_id"]] or 'Unlabelled'

        return clustered_summaries

if __name__=="__main__":
    
    labeler = ClusterLabeler()
    labeled_data, cluster_labels = labeler.label_clusters(clustered)

    for item in labeled_data[:3]:
        print(f"[{item['cluster_id']}] {item['cluster_label']} → {item['summary'][:100]}")
