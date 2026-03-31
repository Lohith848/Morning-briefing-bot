"""
briefing.py — Assembles all data into the final morning briefing message.
v2.0 — Added: fitness tip, word of the day, crypto snapshot, day-progress,
              improved weather (UV + sunrise/sunset), richer formatting.
"""

import concurrent.futures
from datetime import datetime, date

from src.weather      import get_weather
from src.news         import get_news
from src.quotes       import get_quote
from src.tasks        import get_tasks
from src.fitness      import get_fitness_tip
from src.word_of_day  import get_word_of_day
from src.crypto       import get_crypto_snapshot
from src.config       import GROQ_API_KEY, WEATHER_CITY
from src.logger       import log, log_success, log_error


DIV = "━━━━━━━━━━━━━━━━━━━━━━"


# ── Day / Year progress helpers ───────────────────────────────────────────────

def _day_progress() -> str:
    """Returns a mini stats block: week day position & year completion %."""
    today        = date.today()
    day_of_year  = today.timetuple().tm_yday
    days_in_year = 366 if (today.year % 4 == 0 and
                           (today.year % 100 != 0 or today.year % 400 == 0)) else 365
    year_pct     = (day_of_year / days_in_year) * 100

    # Week progress (Mon=1 … Sun=7)
    weekday     = today.isoweekday()           # 1 = Mon, 7 = Sun
    week_labels = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    # Build bar: filled dots for elapsed days, arrow for today, empty for future
    week_bar = "".join(
        "◉" if i + 1 == weekday
        else "●" if i + 1 < weekday
        else "○"
        for i in range(7)
    )
    today_name  = week_labels[weekday - 1]

    # Year bar (20 blocks)
    filled   = round(year_pct / 5)
    year_bar = "█" * filled + "░" * (20 - filled)

    return (
        f"📊 *Day at a Glance*\n"
        f"  Week [{week_bar}]  Today: *{today_name}*\n"
        f"  Year [{year_bar}] *{year_pct:.1f}%* done\n"
        f"  Day *{day_of_year}* of {days_in_year}"
    )


# ── Optional Groq AI insight ──────────────────────────────────────────────────

def _get_ai_insight(headlines: str) -> str:
    """
    Uses Groq (LLaMA 3.1-8b-instant) to generate a short daily insight.
    Completely optional — skipped if GROQ_API_KEY is not set.
    """
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("your_"):
        return ""

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        prompt = (
            f"Based on these headlines:\n{headlines}\n\n"
            "Give me ONE powerful, actionable insight in exactly 2 sentences. "
            "Be sharp, direct, and relevant to a CS student and freelancer in India. "
            "No fluff. No preamble. Just the insight."
        )

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=120,
            temperature=0.7,
        )
        insight = completion.choices[0].message.content.strip()
        log("AI", "Groq insight generated successfully.")
        return f"\n🧠 *AI Insight*\n  {insight}"

    except Exception as e:
        log_error("AI", f"Groq failed: {e}")
        return ""


# ── Main briefing assembler ───────────────────────────────────────────────────

def generate_briefing() -> str:
    """
    Fetches all data in parallel, assembles the full briefing message.
    Returns a Telegram-formatted Markdown string.
    """
    log("BRIEFING", "Starting data fetch…")

    now      = datetime.now()
    day_str  = now.strftime("%A, %B %d %Y")
    time_str = now.strftime("%I:%M %p")
    hour     = now.hour
    greeting = (
        "Good morning"   if 5  <= hour < 12
        else "Good afternoon" if 12 <= hour < 17
        else "Good evening"
    )

    # ── Parallel fetch — all sections simultaneously ───────────────────────
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        f_weather  = pool.submit(get_weather, WEATHER_CITY)
        f_news     = pool.submit(get_news, 5)
        f_quote    = pool.submit(get_quote)
        f_tasks    = pool.submit(get_tasks)
        f_fitness  = pool.submit(get_fitness_tip)
        f_word     = pool.submit(get_word_of_day)
        f_crypto   = pool.submit(get_crypto_snapshot)

        weather  = f_weather.result()
        news     = f_news.result()
        quote    = f_quote.result()
        tasks    = f_tasks.result()
        fitness  = f_fitness.result()
        word     = f_word.result()
        crypto   = f_crypto.result()

    log_success("BRIEFING", "All data fetched successfully.")

    # ── Optional AI block ──────────────────────────────────────────────────
    ai_block    = _get_ai_insight(news)

    # ── Day progress block ─────────────────────────────────────────────────
    day_progress = _day_progress()

    # ── Crypto block (optional — empty string if unavailable) ─────────────
    crypto_block = f"\n{DIV}\n\n{crypto}" if crypto else ""

    # ── Assemble ───────────────────────────────────────────────────────────
    message = (
        f"🌻 *{greeting}, Lohith!*\n\n"
        f"  📅 {day_str} · ⏰ {time_str}\n"
        f"\n{DIV}\n\n"
        f"{day_progress}\n"
        f"\n{DIV}\n\n"
        f"{weather}\n"
        f"\n{DIV}\n\n"
        f"{news}\n"
        f"{ai_block}\n"
        f"\n{DIV}\n\n"
        f"{tasks}\n"
        f"\n{DIV}\n\n"
        f"{fitness}\n"
        f"\n{DIV}\n\n"
        f"{word}\n"
        f"{crypto_block}\n"
        f"\n{DIV}\n\n"
        f"{quote}\n"
        f"\n{DIV}\n"
        f"_Have a productive day! 🚀_"
    )

    log_success("BRIEFING", f"Briefing assembled ({len(message)} chars).")
    return message


# ── Quick preview ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("MORNING BRIEFING BOT v2.0 — Preview Mode")
    print("=" * 55 + "\n")
    briefing = generate_briefing()
    clean = briefing.replace("*", "").replace("_", "")
    print(clean)
