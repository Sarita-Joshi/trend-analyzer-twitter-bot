-- Table to store each ingestion run
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    source TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store raw articles/news/posts
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    source TEXT NOT NULL,              -- e.g., news, reddit, twitter
    source_domain TEXT,                       -- e.g., BBC, r/worldnews, etc.
    title TEXT,
    url TEXT,
    content TEXT,
    published_at TEXT,
    fetched_at TEXT,
    summary TEXT,
    cluster_id INTEGER,
    cluster_label TEXT,
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

-- Table to store poll questions generated from clusters
CREATE TABLE IF NOT EXISTS polls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    cluster_id INTEGER,
    topic TEXT,
    question TEXT,
    options TEXT,  -- JSON string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (run_id) REFERENCES runs(run_id)
);

CREATE TABLE IF NOT EXISTS poll_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tweet_id TEXT,
    run_id TEXT,
    cluster_id INTEGER,
    option_text TEXT,
    vote_percent REAL,
    vote_total TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tweet_id) REFERENCES polls(id)
);
