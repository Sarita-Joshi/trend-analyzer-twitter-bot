# 🧠 TrendPulse: Trending Topic Analyzer & Poll Generator

TrendPulse is an end-to-end automated pipeline that:

- 📰 Ingests trending content from Reddit, Twitter, and News APIs
- ✂️ Summarizes articles using extractive techniques
- 📊 Clusters and labels trending topics
- 🗳️ Generates and posts polls to X (Twitter)
- 📈 Visualizes poll results on a Streamlit dashboard

---

## 🚀 Features

- 🔍 Multi-source ingestion (Reddit, Hacker News, Google News, etc.)
- ✂️ Extractive summarization using TextRank
- 🤖 Embedding + clustering via sentence-transformers + KMeans
- 🏷️ Keyword-based cluster labeling
- 🗳️ Auto poll generation and X API integration
- 📊 Poll result scraping using BeautifulSoup
- 🖥️ Streamlit dashboard with visual analytics
- ⏰ Cron-ready for automation

---

## 🧪 Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize DB (once)
python setup.py

# Run ingestion + summarization + poll generation pipeline
python src/pipeline.py --run_id 2024-06-17-01

# Scrape poll results after 24h
python cron/batch_scraper.py

# Launch dashboard
streamlit run dashboard/app.py
```

---

## 📦 Project Structure

```
trendpulse/
├── src/            # Core logic: ingestion, summarizer, poller
├── cron/           # Scheduled scripts
├── dashboard/      # Streamlit dashboard
├── data/           # Optional local data storage (can be ignored in prod)
├── requirements.txt
├── setup.py
├── render.yaml     # For deployment
├── .env            # Secrets (use env vars in Render)
```

---

## ☁️ Deployment

### On Render (Recommended)
- Add `render.yaml` to root
- Connect GitHub repo to [Render](https://render.com/)
- Set Python Web Service:
  - Build command: `pip install -r requirements.txt`
  - Start command: `streamlit run dashboard/app.py --server.port=$PORT --server.enableCORS false`

### ⏰ Cron Job
- Deploy `cron/batch_scraper.py` as a background worker or cron job

---

## 🔐 Environment Variables
Create a `.env` or configure these in Render:

```env
X_API_KEY=...
X_API_SECRET=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
```

---

## 📊 Dashboard Preview
- Filter by run and cluster
- View vote distributions
- See poll metadata and results in real-time

---

## Future Ideas
- Add OpenAI/Gemini summarization fallback
- Deploy with PostgreSQL for persistent storage
- Slack/Discord notifications for new trends

---

## 👩‍💻 Built With
- Python · Streamlit · SQLite · sentence-transformers · Tweepy · BeautifulSoup

---

## © 2024 TrendPulse
Feel free to fork, modify, or contribute!
