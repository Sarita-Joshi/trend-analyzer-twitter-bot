-- Table to store each ingestion run
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    topic TEXT,
    started_at TEXT,
    ended_at TEXT,
    status TEXT,           -- success | failed
    poll_id TEXT,
    poll_status TEXT       -- active | complete | error
);


-- Table to store raw articles/news/posts
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    source TEXT NOT NULL,            -- e.g., Google News, Reddit
    source_domain TEXT,              -- e.g., cnn.com, r/worldnews
    url TEXT,                        -- Original link (can be NULL)
    resolved_url TEXT,               -- Final link (if resolved)
    title TEXT NOT NULL,             -- Headline/title is required
    content TEXT,
    published_at TEXT,               -- ISO format string
    fetched_at TEXT DEFAULT CURRENT_TIMESTAMP,                -- Set at time of ingestion
    summary TEXT,
    summary_extractive TEXT,
    keywords TEXT,                   -- Optional comma-separated string
    author TEXT,
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
