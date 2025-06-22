from src.summarizer.clusterer import SummaryClusterer

def test_clustering_labels():
    docs = ["AI in cars", "AI in medicine", "Stock market news"]
    ce = SummaryClusterer()
    clusters = ce.cluster(docs)
    assert isinstance(clusters, list)
    assert len(clusters) == len(docs)