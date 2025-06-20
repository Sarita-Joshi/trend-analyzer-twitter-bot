from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from db.db_manager import DBManager

class ExtractiveSummarizer:
    def __init__(self, sentence_count: int = 3):
        self.sentence_count = sentence_count
        self.db = DBManager()
        self.summarizer = TextRankSummarizer()
    
    def summarize_text(self, text: str) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary = self.summarizer(parser.document, self.sentence_count)
        return " ".join([str(sentence) for sentence in summary])

    def summarize_articles(self, run_id: str, persist: bool = False):
        articles = self.db.fetch_articles_by_run_id(run_id)
        results = []

        for article in articles:
            summary = self.summarize_text(article["text"])
            results.append({
                "id": article["id"],
                "summary": summary
            })

            if persist:
                self.db.update_summary(article["id"], summary)

        return results


if __name__ == "__main__":

    from summarizer.extractive import ExtractiveSummarizer

    summarizer = ExtractiveSummarizer(sentence_count=3)
    summaries = summarizer.summarize_articles(run_id="2024-06-17-01", persist=True)

    for item in summaries:
        print(f"[{item['id']}] {item['summary'][:80]}...")

