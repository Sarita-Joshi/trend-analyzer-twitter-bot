from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from src.db.db_manager import DBManager

class ExtractiveSummarizer:
    def __init__(self, sentence_count: int = 3):
        self.sentence_count = sentence_count
        self.db = DBManager()
        self.summarizer = TextRankSummarizer()
    
    def summarize_text(self, text: str) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(parser.document, self.sentence_count)
        return " ".join([str(sentence) for sentence in summary])

    def summarize_articles(self, articles):
        results = []

        for article in articles:
            summary = self.summarize_text(article.content)
            article.summary_extractive = summary
            results.append({
                "id": article.id,
                "summary": summary
            })
        return results


if __name__ == "__main__":

    from summarizer.extractive import ExtractiveSummarizer

    summarizer = ExtractiveSummarizer(sentence_count=3)
    summaries = summarizer.summarize_articles([])

    for item in summaries:
        print(f"[{item['id']}] {item['summary'][:80]}...")

