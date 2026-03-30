"""
tasks.py — Reads today's tasks from a local text file.
Format: One task per line. Lines starting with # are comments.
"""

import os
from datetime import date
from src.config import TASKS_FILE
from src.logger import log


def get_tasks() -> str:
    """
    Reads tasks from TASKS_FILE.
    Returns a formatted string, or a default message if empty/missing.
    """
    path = TASKS_FILE

    if not os.path.exists(path):
        # Create a sample file on first run
        _create_sample_tasks(path)
        log("TASKS", f"Created sample tasks file at {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        tasks = [
            line.strip()
            for line in lines
            if line.strip() and not line.strip().startswith("#")
        ]

        if not tasks:
            return "✅ *Today's Tasks*\n  No tasks set. Edit tasks.txt to add some!"

        items = "\n".join(f"  ☐ {t}" for t in tasks)
        return f"✅ *Today's Tasks* ({len(tasks)} items)\n{items}"

    except Exception as e:
        log("TASKS", f"Error reading tasks: {e}")
        return "✅ *Today's Tasks*\n  Could not read tasks file."


def _create_sample_tasks(path: str):
    """Creates a sample tasks.txt if none exists."""
    sample = f"""\
# Morning Briefing Bot — Tasks File
# Add one task per line. Lines starting with # are ignored.
# Edit this file anytime — changes reflect the next morning.

# Today: {date.today().strftime('%A, %B %d %Y')}
Review yesterday's code
Check emails and respond
Work on current freelance project
Take a 20-min walk
Read for 30 minutes
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(sample)
