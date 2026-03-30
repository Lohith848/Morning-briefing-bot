#!/usr/bin/env python3
"""
main.py — Entry point for Morning Briefing Bot.

Usage:
  python main.py              → Start scheduler (runs daily at configured time)
  python main.py --now        → Send briefing right now + start scheduler
  python main.py --preview    → Preview briefing in terminal (no Telegram send)
  python main.py --test       → Test Telegram connection
  python main.py --check      → Check API config status
"""

import sys
import os

# ── Ensure project root is in path ───────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import validate_config, BRIEFING_TIME, WEATHER_CITY, NEWS_COUNTRY
from src.logger import log, log_error


def cmd_check():
    """Check config validity and show status."""
    print("\n🔍 Configuration Check")
    print("─" * 40)

    from src.config import (
        WEATHER_API_KEY, NEWS_API_KEY, GROQ_API_KEY,
        TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
        WEATHER_CITY, BRIEFING_TIME,
    )

    def status(val, name):
        if val and not val.startswith("your_"):
            print(f"  ✅ {name}: Set")
        else:
            print(f"  ❌ {name}: NOT SET")

    status(WEATHER_API_KEY,    "WEATHER_API_KEY   ")
    status(NEWS_API_KEY,       "NEWS_API_KEY      ")
    status(TELEGRAM_BOT_TOKEN, "TELEGRAM_BOT_TOKEN")
    status(TELEGRAM_CHAT_ID,   "TELEGRAM_CHAT_ID  ")
    status(GROQ_API_KEY,       "GROQ_API_KEY (opt)")

    print(f"\n  📍 City       : {WEATHER_CITY}")
    print(f"  ⏰ Schedule   : {BRIEFING_TIME} daily (IST)")
    print()

    missing = validate_config()
    if missing:
        print(f"  ⚠️  Missing keys: {', '.join(missing)}")
        print("  → Copy .env.example to .env and fill in your keys.\n")
    else:
        print("  ✅ All required keys are set. You're good to go!\n")


def cmd_preview():
    """Preview the briefing in the terminal."""
    print("\n🌅 Generating briefing preview…\n")
    from src.briefing import generate_briefing
    msg = generate_briefing()
    clean = msg.replace("*", "").replace("_", "")
    print(clean)


def cmd_test():
    """Test Telegram connection."""
    print("\n📡 Testing Telegram connection…")
    from src.telegram_sender import test_connection
    ok = test_connection()
    if ok:
        print("  ✅ Telegram connection OK! Check your chat.\n")
    else:
        print("  ❌ Telegram delivery failed. Check your token and chat ID.\n")


def cmd_start(send_now: bool = False):
    """Start the scheduler."""
    missing = validate_config()
    if missing:
        print(f"\n❌ Cannot start: missing config keys: {', '.join(missing)}")
        print("   Run: python main.py --check\n")
        sys.exit(1)

    from src.scheduler import start_scheduler
    start_scheduler(send_now=send_now)


# ── CLI dispatch ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if "--check" in args:
        cmd_check()
    elif "--preview" in args:
        cmd_preview()
    elif "--test" in args:
        cmd_test()
    elif "--now" in args:
        cmd_start(send_now=True)
    else:
        cmd_start(send_now=False)
