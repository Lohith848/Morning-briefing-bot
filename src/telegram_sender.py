"""
telegram_sender.py — Sends messages to Telegram with retry logic.
Uses the raw Bot API (no heavy library needed beyond requests).
"""

import requests
import time
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from src.logger import log, log_success, log_error


TELEGRAM_URL = "https://api.telegram.org/bot{token}/sendMessage"
MAX_RETRIES  = 3
RETRY_DELAY  = 5  # seconds


def send_message(text: str, parse_mode: str = "Markdown") -> bool:
    """
    Sends a message to the configured Telegram chat.
    Retries up to MAX_RETRIES times on failure.
    Returns True on success, False on total failure.
    """
    if not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN.startswith("your_"):
        log("TELEGRAM", "Bot token not set — printing to console instead.")
        print("\n" + "─" * 50)
        print(text.replace("*", "").replace("_", ""))
        print("─" * 50 + "\n")
        return True

    url = TELEGRAM_URL.format(token=TELEGRAM_BOT_TOKEN)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(
                url,
                json={
                    "chat_id":    TELEGRAM_CHAT_ID,
                    "text":       text,
                    "parse_mode": parse_mode,
                },
                timeout=10,
            )

            if resp.status_code == 200:
                log_success("TELEGRAM", f"Message delivered (attempt {attempt}).")
                return True

            data = resp.json()
            err  = data.get("description", "Unknown error")

            # 400 = bad request (wrong chat_id etc.) — don't retry
            if resp.status_code == 400:
                log_error("TELEGRAM", f"Bad request: {err}")
                return False

            # 429 = rate limited — wait longer
            if resp.status_code == 429:
                wait = data.get("parameters", {}).get("retry_after", RETRY_DELAY * 2)
                log("TELEGRAM", f"Rate limited. Waiting {wait}s…")
                time.sleep(wait)
                continue

            log("TELEGRAM", f"Attempt {attempt} failed ({resp.status_code}): {err}")

        except requests.exceptions.ConnectionError:
            log_error("TELEGRAM", f"No connection (attempt {attempt}).")
        except requests.exceptions.Timeout:
            log_error("TELEGRAM", f"Timeout (attempt {attempt}).")
        except Exception as e:
            log_error("TELEGRAM", f"Unexpected error: {e}")

        if attempt < MAX_RETRIES:
            log("TELEGRAM", f"Retrying in {RETRY_DELAY}s…")
            time.sleep(RETRY_DELAY)

    log_error("TELEGRAM", "All delivery attempts failed.")
    return False


def test_connection() -> bool:
    """Sends a test ping to verify the bot is working."""
    return send_message(
        "✅ *Morning Briefing Bot is online!*\nYou'll receive your briefing every morning.",
    )
