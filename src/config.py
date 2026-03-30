import os

# Try loading .env (works locally, ignored in GitHub)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# ── API Keys ─────────────────────────
WEATHER_API_KEY  = os.getenv("WEATHER_API_KEY", "")
NEWS_API_KEY     = os.getenv("NEWS_API_KEY", "")
GROQ_API_KEY     = os.getenv("GROQ_API_KEY", "")

# ── Telegram ─────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID   = os.getenv("CHAT_ID", "")

# ── Preferences ──────────────────────
WEATHER_CITY   = os.getenv("WEATHER_CITY", "Coimbatore")
NEWS_COUNTRY   = os.getenv("NEWS_COUNTRY", "in")
BRIEFING_TIME  = os.getenv("BRIEFING_TIME", "07:00")
TASKS_FILE     = os.getenv("TASKS_FILE", "tasks.txt")

# ── Validation ───────────────────────
def validate_config():
    missing = []

    if not WEATHER_API_KEY:
        missing.append("WEATHER_API_KEY")
    if not NEWS_API_KEY:
        missing.append("NEWS_API_KEY")
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("CHAT_ID")

    return missing