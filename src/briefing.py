"""
briefing.py — Assembles all data into the final morning briefing message.
Optionally uses Groq (LLaMA 3.1) to add an AI-generated daily insight.
"""

import concurrent.futures
from datetime import datetime

from src.weather import get_weather
from src.news    import get_news
from src.quotes  import get_quote
from src.tasks   import get_tasks
from src.config  import GROQ_API_KEY, WEATHER_CITY
from src.logger  import log, log_success, log_error


# ── Optional Groq AI insight ──────────────────────────────────────────────────

def _get_ai_insight(headlines: str) -> str:
    """
    Uses Groq (LLaMA 3.1-8b-instant) to generate a short, punchy daily insight.
    Completely optional — skipped if GROQ_API_KEY is not set.
    """
    if not GROQ_API_KEY or GROQ_API_KEY.startswith("your_"):
        return ""

    try:
        from groq import Groq  # lazy import — won't crash if not installed
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
    Fetches all data in parallel, assembles the briefing message.
    Returns a Telegram-formatted string (Markdown).
    """
    log("BRIEFING", "Starting data fetch…")

    now         = datetime.now()
    day_str     = now.strftime("%A, %B %d %Y")
    time_str    = now.strftime("%I:%M %p")
    hour        = now.hour
    greeting    = (
        "Good morning" if 5 <= hour < 12
        else "Good afternoon" if 12 <= hour < 17
        else "Good evening"
    )

    # ── Parallel fetch (faster than sequential) ────────────────────────────
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        f_weather = pool.submit(get_weather, WEATHER_CITY)
        f_news    = pool.submit(get_news, 5)
        f_quote   = pool.submit(get_quote)
        f_tasks   = pool.submit(get_tasks)

        weather = f_weather.result()
        news    = f_news.result()
        quote   = f_quote.result()
        tasks   = f_tasks.result()

    log_success("BRIEFING", "All data fetched successfully.")

    # ── Optional AI insight ────────────────────────────────────────────────
    ai_block = _get_ai_insight(news)

    # ── Assemble message ───────────────────────────────────────────────────
    divider = "━━━━━━━━━━━━━━━━━━━━━━"

    message = (
        f"🌻*{greeting}, Lohith!*\n"
        f"  {day_str} · {time_str}\n"
        f"\n{divider}\n\n"
        f"{weather}\n"
        f"\n{divider}\n\n"
        f"{news}\n"
        f"\n{divider}\n\n"
        f"{tasks}\n"
        f"\n{divider}\n\n"
        f"{quote}"
        f"{ai_block}\n"
        f"\n{divider}\n"
        f"_Have a productive day! 🚀_"
    )

    log_success("BRIEFING", f"Briefing assembled ({len(message)} chars).")
    return message


# ── Quick preview (run this file directly) ────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("MORNING BRIEFING BOT — Preview Mode")
    print("=" * 50 + "\n")
    briefing = generate_briefing()
    # Strip Telegram markdown for cleaner terminal output
    clean = briefing.replace("*", "").replace("_", "")
    print(clean)
