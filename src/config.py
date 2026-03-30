"""
config.py — Central configuration loader.
Reads from .env file. All modules import from here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────
WEATHER_API_KEY  = os.getenv("WEATHER_API_KEY", "")
NEWS_API_KEY     = os.getenv("NEWS_API_KEY", "")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY", "")

# ── Telegram ──────────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID", "")

# ── Preferences ───────────────────────────────────────────
WEATHER_CITY   = os.getenv("WEATHER_CITY", "Coimbatore")
NEWS_COUNTRY   = os.getenv("NEWS_COUNTRY", "in")
BRIEFING_TIME  = os.getenv("BRIEFING_TIME", "07:00")
TASKS_FILE     = os.getenv("TASKS_FILE", "tasks.txt")

# ── Validation ────────────────────────────────────────────
def validate_config() -> list[str]:
    """Returns a list of missing required keys."""
    missing = []
    required = {
        "WEATHER_API_KEY":    WEATHER_API_KEY,
        "NEWS_API_KEY":       NEWS_API_KEY,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "TELEGRAM_CHAT_ID":   TELEGRAM_CHAT_ID,
    }
    for name, val in required.items():
        if not val or val.startswith("your_"):
            missing.append(name)
    return missing
