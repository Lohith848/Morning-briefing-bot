# Morning Briefing Bot

A GitHub Actions–powered Telegram bot that sends you a rich daily morning briefing every day at **~7:00 AM IST**.

---

## What You Get Every Morning

| Section | Details |
|---|---|
| 📊 **Day at a Glance** | Week bar, year-progress bar, day number |
| ☀️ **Weather** | Temp, feels-like, humidity, wind, UV index, sunrise & sunset |
| 📰 **Top Headlines** | 5 Indian news headlines (NewsAPI → BBC RSS fallback) |
| 🧠 **AI Insight** _(optional)_ | Groq LLaMA-generated insight based on today's news |
| ✅ **Today's Tasks** | Read from `tasks.txt` in the repo |
| 🏋️ **Wellness Tip** | Daily rotating fitness/health tip (no API needed) |
| 📚 **Word of the Day** | Daily vocabulary builder with definition & example |
| 💰 **Crypto Snapshot** | Live BTC & ETH prices in INR with 24h change (CoinGecko, no key needed) |
| 💡 **Quote of the Day** | Motivational quote (quotable.io → curated fallback) |

---

## Timing — Why it Sometimes Arrives Late

GitHub Actions uses **UTC** and free-tier runners can **delay up to 15–30 minutes** under load.

| Setting | Value |
|---|---|
| Cron schedule | `0 1 * * *` (1:00 AM UTC) |
| Equivalent IST | **6:30 AM IST** |
| Expected arrival | **~7:00 AM IST** (30-min buffer for runner queue) |

> **If it still arrives late:** This is a GitHub limitation. Upgrade to a paid plan or self-host a runner for exact timing.

---

## Setup

### 1. Fork / Clone this repo

```bash
git clone https://github.com/YOUR_USERNAME/morning-briefing-bot
cd morning-briefing-bot
```

### 2. Set GitHub Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**:

| Secret Name | Where to get it |
|---|---|
| `TELEGRAM_TOKEN` | [@BotFather](https://t.me/BotFather) on Telegram |
| `CHAT_ID` | [@userinfobot](https://t.me/userinfobot) on Telegram |
| `WEATHER_API_KEY` | [openweathermap.org](https://openweathermap.org/api) (free tier) |
| `NEWS_API_KEY` | [newsapi.org](https://newsapi.org) (free tier) |
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) _(optional — for AI insight)_ |
| `WEATHER_CITY` | Your city name e.g. `Coimbatore` _(optional, defaults to Coimbatore)_ |

### 3. Edit your tasks

Edit `tasks.txt` — one task per line. Lines starting with `#` are comments.

```
# tasks.txt
Review PR before 10am
Finish freelance invoice
30-minute algorithm practice
Evening walk
```

### 4. Enable GitHub Actions

Go to **Actions tab** → Enable workflows → The bot runs automatically every morning.

You can also trigger it manually: **Actions → Morning Briefing Bot → Run workflow**.

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Copy env example and fill in your keys
cp .env.example .env

# Preview briefing in terminal (no Telegram send)
python main.py --preview

# Test Telegram connection
python main.py --test

# Check all config keys
python main.py --check

# Send briefing now
python main.py
```

---

## 📁 Project Structure

```
morning-briefing-bot/
├── main.py                   # Entry point & CLI
├── tasks.txt                 # Your daily task list
├── requirements.txt
├── .env.example
├── .github/
│   └── workflows/
│       └── morning.yml       # GitHub Actions schedule
└── src/
    ├── briefing.py           # Assembles the full message
    ├── weather.py            # OpenWeatherMap (temp, UV, sunrise/sunset)
    ├── news.py               # NewsAPI + BBC RSS fallback
    ├── quotes.py             # quotable.io + curated fallback
    ├── tasks.py              # Reads tasks.txt
    ├── fitness.py            # 🆕 Daily wellness tip (no API)
    ├── word_of_day.py        # 🆕 Daily vocabulary word (no API)
    ├── crypto.py             # 🆕 BTC/ETH prices via CoinGecko (no API key)
    ├── config.py             # Env var loading
    ├── logger.py             # Simple logger
    └── telegram_sender.py    # Sends message with retry logic
```

---

## API Keys Summary

| Service | Required | Free Tier | Key Name |
|---|---|---|---|
| OpenWeatherMap | ✅ Yes | ✅ Yes (1000 calls/day) | `WEATHER_API_KEY` |
| NewsAPI | ✅ Yes | ✅ Yes (100 calls/day) | `NEWS_API_KEY` |
| Telegram Bot | ✅ Yes | ✅ Free | `TELEGRAM_TOKEN` + `CHAT_ID` |
| CoinGecko | ❌ No key needed | ✅ Free | — |
| Groq (LLaMA AI) | ❌ Optional | ✅ Free | `GROQ_API_KEY` |

---

## 📋 Sample Briefing Output

```
🌻 Good morning, Lohith!
  📅 Tuesday, March 31 2026 · ⏰ 07:00 AM

━━━━━━━━━━━━━━━━━━━━━━

📊 Day at a Glance
  Week [●●◉○○○○]  Today: Tue
  Year [████░░░░░░░░░░░░░░░░] 24.6% done
  Day 91 of 365

━━━━━━━━━━━━━━━━━━━━━━

☀️ Weather in Coimbatore
  🌡️ 31°C (feels like 35°C)
  Haze | 💧 Humidity: 68%
  💨 Wind: 14 km/h
  ☀️ UV Index: 🔴 Very High (9)
  🌅 Sunrise: 06:18 AM · 🌇 Sunset: 06:32 PM

━━━━━━━━━━━━━━━━━━━━━━

📰 Top Headlines
  1. India's tech sector grows 18% YoY...
  ...

✅ Today's Tasks (3 items)
  ☐ Review PR before 10am
  ☐ Finish freelance invoice
  ☐ 30-minute algorithm practice

🏋️ Wellness Tip  Hydration
  💧 Drink a full glass of water right now — your body is 10% dehydrated after sleep.

📚 Word of the Day
  Tenacious (adj)
  Holding firmly to purpose; persistent.
  📝 "His tenacious work ethic made him irreplaceable."

💰 Crypto Snapshot (24h change)
  ₿ BTC: ₹72,45,300  🚀 +4.2%
  Ξ ETH: ₹2,81,500   📈 +1.8%

💡 Quote of the Day
  "The secret of getting ahead is getting started."
  — Mark Twain

━━━━━━━━━━━━━━━━━━━━━━
Have a productive day! 🚀
```

---

## 🤝 Made by 
Lohith G