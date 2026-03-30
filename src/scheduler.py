"""
scheduler.py — Reliable daily scheduler using APScheduler.
More robust than the `schedule` library — handles system sleep/wake properly.
"""

import signal
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron       import CronTrigger

from src.config          import BRIEFING_TIME
from src.briefing        import generate_briefing
from src.telegram_sender import send_message
from src.logger          import log, log_success, log_error


def run_briefing():
    """Core job: generate and send the briefing."""
    log("SCHEDULER", f"Triggering briefing at {datetime.now().strftime('%H:%M:%S')}")
    try:
        message = generate_briefing()
        success = send_message(message)
        if success:
            log_success("SCHEDULER", "Briefing sent successfully ✓")
        else:
            log_error("SCHEDULER", "Briefing generated but delivery failed.")
    except Exception as e:
        log_error("SCHEDULER", f"Briefing job crashed: {e}")


def start_scheduler(send_now: bool = False):
    """
    Starts the blocking scheduler.
    If send_now=True, fires an immediate briefing before waiting for schedule.
    """
    hour, minute = BRIEFING_TIME.split(":")

    log("SCHEDULER", f"Morning Briefing Bot starting…")
    log("SCHEDULER", f"Scheduled time: {BRIEFING_TIME} daily")
    log("SCHEDULER", "Press Ctrl+C to stop.")

    if send_now:
        log("SCHEDULER", "Sending immediate briefing (--now flag)…")
        run_briefing()

    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        run_briefing,
        trigger=CronTrigger(hour=int(hour), minute=int(minute)),
        id="morning_briefing",
        name="Daily Morning Briefing",
        misfire_grace_time=600,  # allow up to 10min late firing
        coalesce=True,           # don't stack missed runs
    )

    # ── Graceful shutdown on Ctrl+C / kill ────────────────
    def shutdown(sig, frame):
        log("SCHEDULER", "Shutdown signal received. Stopping…")
        scheduler.shutdown(wait=False)
        sys.exit(0)

    signal.signal(signal.SIGINT,  shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    scheduler.start()
