import feedparser
from datetime import datetime
from newspaper import Article

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from src.schemas.article_schema import ArticleSchema


class GoogleNewsIngestor:
    def __init__(self, run_id, query="AI", max_articles=10):
        self.run_id = run_id
        self.query = query
        self.feed_url = f"https://news.google.com/rss/search?q={query}"
        self.max_articles = max_articles

    def create_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("user-agent=Mozilla/5.0")

        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        
    def _resolve_redirect(self, url: str) -> str:
        """Use shared headless driver to resolve real article URL."""
        try:
            self.driver.get(url)
            time.sleep(1.5)
            return self.driver.current_url
        except Exception:
            return url  # fallback to original if failure

    def fetch(self):
        try:
            self.create_driver()
            feed = feedparser.parse(self.feed_url)
            articles = []
            
            for entry in feed.entries[:self.max_articles]:
                original_link = entry.link
                try:
                    resolved_url = self._resolve_redirect(original_link)
                    article = Article(resolved_url)
                    article.download()
                    article.parse()
                    article.nlp()
                    content = article.text.strip()
                    summary = article.summary
                except Exception as e:
                    content = f"Error fetching content: {e}"
                    summary = entry.get("summary", "")

                article = ArticleSchema(
                    run_id=self.run_id,
                    source="Google News",
                    source_domain=entry.source,
                    url=entry.link,
                    resolved_url=resolved_url,
                    title=entry.title,
                    content=content,
                    summary=summary,
                    published_at=datetime(*entry.published_parsed[:6]).isoformat(),
                )

                articles.append(article)

            return articles
        finally:
            self.driver.quit()

    def close(self):
        self.driver.quit()


# Example usage
if __name__ == "__main__":
    ingestor = GoogleNewsIngestor("AI", max_articles=1)
    try:
        articles = ingestor.fetch()
        for art in articles:
            print(f"\n📰 {art['title']}\n🔗 {art['resolved_url']}\n📄 {art['content'][:120]}...\n")
    finally:
        ingestor.close()
