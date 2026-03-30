"""
news.py — Fetches top headlines from NewsAPI (free tier).
Falls back to BBC RSS feed if NewsAPI fails (always-free backup).
"""

import requests
import xml.etree.ElementTree as ET
from src.config import NEWS_API_KEY, NEWS_COUNTRY
from src.logger import log


NEWSAPI_URL  = "https://newsapi.org/v2/top-headlines"
BBC_RSS_URL  = "https://feeds.bbci.co.uk/news/world/rss.xml"
INDIA_RSS    = "https://feeds.feedburner.com/ndtvnews-india-news"


def _fetch_newsapi(count: int = 5) -> list[str]:
    """Primary source: NewsAPI."""
    resp = requests.get(
        NEWSAPI_URL,
        params={
            "country": NEWS_COUNTRY,
            "apiKey":  NEWS_API_KEY,
            "pageSize": count,
        },
        timeout=8,
    )
    resp.raise_for_status()
    data = resp.json()

    if data.get("status") != "ok":
        raise ValueError(f"NewsAPI error: {data.get('message', 'unknown')}")

    articles = data.get("articles", [])
    headlines = []
    for a in articles[:count]:
        title  = a.get("title", "").strip()
        source = a.get("source", {}).get("name", "")
        if title and "[Removed]" not in title:
            headlines.append(f"{title} — _{source}_" if source else title)

    return headlines


def _fetch_rss(url: str, count: int = 5) -> list[str]:
    """Fallback source: RSS feed (always free, no key needed)."""
    resp = requests.get(url, timeout=8, headers={"User-Agent": "MorningBot/1.0"})
    resp.raise_for_status()

    root = ET.fromstring(resp.content)
    items = root.findall(".//item")[:count]

    headlines = []
    for item in items:
        title = item.findtext("title", "").strip()
        if title:
            headlines.append(title)

    return headlines


def get_news(count: int = 5) -> str:
    """
    Returns a formatted news block with top headlines.
    Tries NewsAPI first, falls back to BBC RSS.
    """
    headlines = []
    source_label = ""

    # ── Attempt 1: NewsAPI ────────────────────────────────
    if NEWS_API_KEY and not NEWS_API_KEY.startswith("your_"):
        try:
            headlines = _fetch_newsapi(count)
            source_label = "via NewsAPI"
            log("NEWS", f"Fetched {len(headlines)} headlines from NewsAPI")
        except Exception as e:
            log("NEWS", f"NewsAPI failed ({e}), falling back to RSS…")

    # ── Attempt 2: BBC RSS (free, no key) ─────────────────
    if not headlines:
        try:
            headlines = _fetch_rss(BBC_RSS_URL, count)
            source_label = "via BBC RSS"
            log("NEWS", f"Fetched {len(headlines)} headlines from BBC RSS")
        except Exception as e:
            log("NEWS", f"BBC RSS also failed: {e}")
            return "📰 *Top Headlines*\n  News unavailable right now."

    lines = "\n".join(f"  {i}. {h}" for i, h in enumerate(headlines, 1))
    footer = f"\n  _{source_label}_" if source_label else ""
    return f"📰 *Top Headlines*\n{lines}{footer}"
