#!/usr/bin/env python3
"""
main.py — Entry point for Morning Briefing Bot (GitHub Actions optimized)

Usage:
  python main.py              → Send briefing once (default for GitHub)
  python main.py --preview    → Preview briefing in terminal
  python main.py --test       → Test Telegram connection
  python main.py --check      → Check API config status
"""

import sys
import os

# ── Ensure project root is in path ───────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import validate_config, BRIEFING_TIME, WEATHER_CITY
from src.logger import log, log_error


def cmd_check():
    print("\n🔍 Configuration Check")
    print("─" * 40)

    from src.config import (
        WEATHER_API_KEY, NEWS_API_KEY, GROQ_API_KEY,
        TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
    )

    def status(val, name):
        if val:
            print(f"  ✅ {name}: Set")
        else:
            print(f"  ❌ {name}: NOT SET")

    status(WEATHER_API_KEY, "WEATHER_API_KEY")
    status(NEWS_API_KEY, "NEWS_API_KEY")
    status(TELEGRAM_BOT_TOKEN, "TELEGRAM_TOKEN")
    status(TELEGRAM_CHAT_ID, "CHAT_ID")
    status(GROQ_API_KEY, "GROQ_API_KEY (optional)")

    print(f"\n  📍 City     : {WEATHER_CITY}")
    print(f"  ⏰ Schedule : {BRIEFING_TIME} daily\n")

    missing = validate_config()
    if missing:
        print(f"⚠️ Missing: {', '.join(missing)}\n")
    else:
        print("✅ All good!\n")


def cmd_preview():
    print("\n🌅 Previewing briefing...\n")
    from src.briefing import generate_briefing
    msg = generate_briefing()
    print(msg)


def cmd_test():
    print("\n📡 Testing Telegram...")
    from src.telegram_sender import test_connection
    if test_connection():
        print("✅ Telegram working!\n")
    else:
        print("❌ Telegram failed\n")


def send_once():
    """Main function for GitHub Actions (run once and exit)"""
    missing = validate_config()
    if missing:
        print(f"❌ Missing config: {', '.join(missing)}")
        sys.exit(1)

    try:
        from src.briefing import generate_briefing
        from src.telegram_sender import send_message

        print("🚀 Generating briefing...")
        msg = generate_briefing()

        print("📤 Sending to Telegram...")
        send_message(msg)

        print("✅ Done successfully!")

    except Exception as e:
        print("❌ Error:", str(e))
        sys.exit(1)


# ── CLI ─────────────────────────────────────────────────
if __name__ == "__main__":
    args = sys.argv[1:]

    if "--check" in args:
        cmd_check()
    elif "--preview" in args:
        cmd_preview()
    elif "--test" in args:
        cmd_test()
    else:
        send_once()   # 🔥 ALWAYS run once (important)