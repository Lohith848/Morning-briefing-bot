# 🌅 Morning Briefing Bot

A personalized daily briefing bot that delivers **weather, news, tasks, and a motivational quote** every morning via Telegram — with optional AI insights via Groq (LLaMA 3.1).

---

## ✨ Features

| Feature | Source | Free? |
|---|---|---|
| 🌤 Weather | OpenWeatherMap API | ✅ Free tier |
| 📰 News | NewsAPI → BBC RSS fallback | ✅ Free tier |
| 💡 Quote | quotable.io → built-in fallback | ✅ Always free |
| ✅ Tasks | Local `tasks.txt` file | ✅ Always free |
| 🧠 AI Insight | Groq (LLaMA 3.1-8b-instant) | ✅ Free tier |
| 📲 Delivery | Telegram Bot | ✅ Always free |

---

## 🚀 Quick Start (5 Steps)

### Step 1 — Clone & Install

```bash
git clone <your-repo-url>
cd morning-briefing-bot
pip install -r requirements.txt
```

### Step 2 — Get Your Free API Keys

| Key | Where to get it | Time |
|---|---|---|
| OpenWeatherMap | https://openweathermap.org/api → "Get API Key" | 2 min |
| NewsAPI | https://newsapi.org/register | 1 min |
| Telegram Bot | Message `@BotFather` → `/newbot` | 2 min |
| Telegram Chat ID | Message `@userinfobot` | 30 sec |
| Groq (optional) | https://console.groq.com | 2 min |

### Step 3 — Configure

```bash
cp .env.example .env
# Now edit .env with your keys
```

Your `.env` file:
```env
WEATHER_API_KEY=abc123...
NEWS_API_KEY=xyz789...
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=987654321
GROQ_API_KEY=gsk_...        # optional — for AI insights
WEATHER_CITY=Coimbatore
BRIEFING_TIME=07:00
```

### Step 4 — Verify Everything Works

```bash
python main.py --check      # Check all API keys are set
python main.py --preview    # See the briefing in terminal
python main.py --test       # Send a test message to Telegram
```

### Step 5 — Run It!

```bash
python main.py              # Start scheduler (runs daily at 07:00)
python main.py --now        # Send immediately + start scheduler
```

---

## 📁 Project Structure

```
morning-briefing-bot/
├── main.py               ← Entry point (all commands)
├── tasks.txt             ← Edit your daily tasks here
├── .env                  ← Your API keys (never commit this)
├── .env.example          ← Template for .env
├── requirements.txt
├── logs/
│   └── briefing.log      ← Auto-created log file
└── src/
    ├── config.py         ← Loads .env, validates keys
    ├── weather.py        ← OpenWeatherMap integration
    ├── news.py           ← NewsAPI + BBC RSS fallback
    ├── quotes.py         ← quotable.io + offline fallback
    ├── tasks.py          ← Reads tasks.txt
    ├── briefing.py       ← Assembles the full message
    ├── telegram_sender.py← Delivers via Telegram (with retries)
    ├── scheduler.py      ← APScheduler daily job
    └── logger.py         ← Clean logging to console + file
```

---

## 🖥 CLI Commands

```bash
python main.py              # Start daily scheduler
python main.py --now        # Send now + start scheduler
python main.py --preview    # Terminal preview (no Telegram)
python main.py --test       # Test Telegram connection
python main.py --check      # Verify config / API keys
```

---

## ✅ How to Edit Your Tasks

Just open `tasks.txt` and edit it:

```
# Lines starting with # are ignored

Review pull requests
Work on freelance project
Gym session at 6pm
Read for 30 minutes
```

Changes take effect the next time the briefing runs.

---

## 🔁 Keep It Running 24/7

### Option A — Linux/Mac (background process)
```bash
nohup python main.py > logs/output.log 2>&1 &
```

### Option B — systemd service (recommended for Linux VPS)
```ini
# /etc/systemd/system/morning-bot.service
[Unit]
Description=Morning Briefing Bot

[Service]
WorkingDirectory=/path/to/morning-briefing-bot
ExecStart=/usr/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable morning-bot
sudo systemctl start morning-bot
```

### Option C — Deploy on Render/Railway (free cloud)
1. Push to GitHub
2. Connect repo to Render (Worker service)
3. Set environment variables in Render dashboard
4. Done — runs forever for free

---

## 🧠 Sample Telegram Message

```
🌅 Good morning, Think!
  Monday, March 30 2026 · 07:00 AM

━━━━━━━━━━━━━━━━━━━━━━

☀️ Weather in Coimbatore
  Temp: 28°C (feels like 31°C)
  Clear sky | Humidity: 65%
  Wind: 12 km/h

━━━━━━━━━━━━━━━━━━━━━━

📰 Top Headlines
  1. Budget 2026 highlights — The Hindu
  2. India's GDP grows 7.2% in Q3 — NDTV
  3. SpaceX launches new satellite cluster — BBC

━━━━━━━━━━━━━━━━━━━━━━

✅ Today's Tasks (4 items)
  ☐ Review yesterday's code commits
  ☐ Check freelance client messages
  ☐ Work on current project for 2 hours
  ☐ Read for 30 minutes before sleep

━━━━━━━━━━━━━━━━━━━━━━

💡 Quote of the Day
  "Small daily improvements lead to stunning results."
  — Robin Sharma

🧠 AI Insight
  India's economic growth signals strong demand for tech
  freelancers — now is the time to raise your rates.

━━━━━━━━━━━━━━━━━━━━━━
Have a productive day! 🚀
```

---

## 🛠 Troubleshooting

| Problem | Fix |
|---|---|
| `WEATHER_API_KEY not set` | Run `--check`, fill `.env` |
| News shows BBC instead of Indian news | Your NewsAPI free tier may be expired |
| Telegram not receiving | Run `--test`, verify token + chat ID |
| Briefing runs at wrong time | Check timezone — set to `Asia/Kolkata` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |

---

## 📈 Roadmap

- [x] Weather, News, Quotes, Tasks
- [x] Groq AI insight
- [x] Telegram delivery with retries
- [x] BBC RSS fallback
- [ ] Voice briefing (pyttsx3 / ElevenLabs)
- [ ] Web dashboard UI
- [ ] WhatsApp delivery (via Cyrus bot)
- [ ] Google Calendar sync
- [ ] Smart topic preferences

---

Built by Think 🧠 | Powered by free APIs
