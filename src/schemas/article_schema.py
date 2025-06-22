from dataclasses import dataclass, field

from typing import Optional, List
import uuid
@dataclass
class ArticleSchema:
    run_id: str                  # Assigned by you before ingestion
    source: str                  # e.g., 'Google News', 'Reddit', 'Twitter'
    url: str                     # Original link
    title: str                   # Article headline
    content: str                 # Full article text
    published_at: str           # ISO format date string
    fetched_at: Optional[str] = None           # ISO format date string

    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    
    resolved_url: Optional[str] = None # Final destination URL after redirects
    source_domain: Optional[str] = None # e.g., cnn.com, timesnews.com, etc
    summary: Optional[str] = None     # Optional LLM or extractive summary
    summary_extractive: Optional[str] = None     # Optional LLM or extractive summary
    
    keywords: Optional[List] = field(default_factory=list)   #Optional article keywords
    author: Optional[str] = None
    cluster_id: Optional[int] = None
    cluster_label: Optional[str] = None

