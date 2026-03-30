"""
quotes.py — Fetches motivational quotes.
Primary: quotable.io (completely free, no API key)
Fallback: Built-in curated list (works offline)
"""

import requests
import random
from src.logger import log


QUOTABLE_URL = "https://api.quotable.io/random"

# Offline fallback pool — diverse, hand-picked
FALLBACK_QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("It always seems impossible until it's done.", "Nelson Mandela"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("You are never too old to set another goal or dream a new dream.", "C.S. Lewis"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Success is not final, failure is not fatal — it's the courage to continue.", "Winston Churchill"),
    ("The harder I work, the luckier I get.", "Samuel Goldwyn"),
    ("Start where you are. Use what you have. Do what you can.", "Arthur Ashe"),
    ("Dream big. Start small. Act now.", "Robin Sharma"),
    ("Your only limit is your mind.", "Unknown"),
    ("Small daily improvements lead to stunning results.", "Robin Sharma"),
    ("The best time to plant a tree was 20 years ago. The second best is today.", "Chinese Proverb"),
    ("First, solve the problem. Then, write the code.", "John Johnson"),
    ("Code is poetry.", "Automattic"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans understand.", "Martin Fowler"),
]


def get_quote() -> str:
    """
    Returns a formatted quote string.
    Tries quotable.io first, falls back to built-in list.
    """
    # ── Attempt: quotable.io ──────────────────────────────
    try:
        resp = requests.get(
            QUOTABLE_URL,
            params={"tags": "motivational|technology|success"},
            timeout=5,
        )
        if resp.status_code == 200:
            data = resp.json()
            content = data.get("content", "").strip()
            author  = data.get("author", "Unknown").strip()
            if content:
                log("QUOTE", f"Fetched from quotable.io")
                return f'💡 *Quote of the Day*\n  "{content}"\n  — _{author}_'
    except Exception as e:
        log("QUOTE", f"quotable.io failed ({e}), using fallback.")

    # ── Fallback: built-in list ───────────────────────────
    content, author = random.choice(FALLBACK_QUOTES)
    return f'💡 *Quote of the Day*\n  "{content}"\n  — _{author}_'
