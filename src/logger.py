"""
logger.py — Minimal, clean logger that writes to console + log file.
No external dependencies needed.
"""

import os
import sys
from datetime import datetime

LOG_DIR  = "logs"
LOG_FILE = os.path.join(LOG_DIR, "briefing.log")


def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def log(module: str, message: str, level: str = "INFO"):
    """
    Logs a message with timestamp and module name.
    Writes to both console and logs/briefing.log
    """
    _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tag       = f"[{level}][{module}]"
    line      = f"{timestamp} {tag:<22} {message}"

    print(line, file=sys.stdout)

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass  # Don't crash the bot over logging


def log_error(module: str, message: str):
    log(module, message, level="ERROR")


def log_success(module: str, message: str):
    log(module, message, level="OK   ")
