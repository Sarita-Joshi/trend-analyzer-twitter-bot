import pytest
from src.summarizer import Summarizer
from src.schemas import ArticleSchema  # or wherever ArticleSchema is defined

@pytest.fixture
def sample_articles():
    return [
        ArticleSchema(
            run_id="test-001",
            source="news",
            url="https://news.com/openai-gpt5",
            title="OpenAI Releases GPT-5",
            content="OpenAI has announced the release of GPT-5 with improved reasoning. Experts believe it will change the AI landscape dramatically.",
            published_at="2024-06-01T08:00:00Z"
        ),
        ArticleSchema(
            run_id="test-001",
            source="news",
            url="https://news.com/ai-regulations",
            title="AI Regulations Introduced",
            content="New government policies aim to ensure safe and ethical AI. These regulations are being discussed worldwide.",
            published_at="2024-06-01T09:00:00Z"
        ),
        ArticleSchema(
            run_id="test-001",
            source="news",
            url="https://sports.com/world-cup",
            title="Sports Update",
            content="The FIFA World Cup has kicked off with a spectacular opening ceremony. Fans are excited and stadiums are packed.",
            published_at="2024-06-01T10:00:00Z"
        ),
    ]

def test_summarizer_pipeline(sample_articles):
    summarizer = Summarizer()
    sentence_data = summarizer.summarize(sample_articles)

    assert isinstance(sentence_data, list), "Expected a list of clustered sentence metadata"
    assert len(sentence_data) > 0, "No sentence data returned"

    for item in sentence_data:
        assert "sentence" in item
        assert "embedding" in item
        assert "cluster_id" in item
        assert "cluster_label" in item
        assert isinstance(item["sentence"], str) and len(item["sentence"]) > 5
        assert isinstance(item["embedding"], list) and len(item["embedding"]) > 0
        assert isinstance(item["cluster_id"], int)
        assert isinstance(item["cluster_label"], str)
