"""
weather.py — Fetches current weather from OpenWeatherMap (free tier).
Includes: temp, feels-like, humidity, wind, UV index, sunrise & sunset.
Endpoint: api.openweathermap.org/data/2.5/weather
"""

import requests
from datetime import datetime, timezone
from src.config import WEATHER_API_KEY, WEATHER_CITY
from src.logger import log


WEATHER_URL    = "https://api.openweathermap.org/data/2.5/weather"
UV_URL         = "https://api.openweathermap.org/data/2.5/uvi"

WEATHER_EMOJI = {
    "clear":        "☀️",
    "clouds":       "☁️",
    "rain":         "🌧️",
    "drizzle":      "🌦️",
    "thunderstorm": "⛈️",
    "snow":         "❄️",
    "mist":         "🌫️",
    "haze":         "🌫️",
    "fog":          "🌫️",
    "smoke":        "💨",
    "dust":         "🌪️",
    "sand":         "🌪️",
}

UV_LABEL = {
    (0, 3):   ("Low",     "🟢"),
    (3, 6):   ("Moderate","🟡"),
    (6, 8):   ("High",    "🟠"),
    (8, 11):  ("Very High","🔴"),
    (11, 99): ("Extreme", "🟣"),
}


def _uv_badge(uv: float) -> str:
    for (lo, hi), (label, dot) in UV_LABEL.items():
        if lo <= uv < hi:
            return f"{dot} {label} ({uv:.0f})"
    return f"({uv:.0f})"


def _fmt_time(unix_ts: int, tz_offset_secs: int) -> str:
    """Convert UTC unix timestamp → local time string using city's UTC offset."""
    local_dt = datetime.fromtimestamp(unix_ts + tz_offset_secs, tz=timezone.utc)
    return local_dt.strftime("%I:%M %p")


def get_weather(city: str = WEATHER_CITY) -> str:
    """
    Returns a richly formatted weather string for the given city.
    Falls back gracefully on any error.
    """
    if not WEATHER_API_KEY:
        return "🌤️ *Weather*\n  API key not set."

    try:
        resp = requests.get(
            WEATHER_URL,
            params={
                "q":     city,
                "appid": WEATHER_API_KEY,
                "units": "metric",
            },
            timeout=8,
        )
        resp.raise_for_status()
        data = resp.json()

        temp        = round(data["main"]["temp"])
        feels_like  = round(data["main"]["feels_like"])
        humidity    = data["main"]["humidity"]
        desc        = data["weather"][0]["description"].capitalize()
        condition   = data["weather"][0]["main"].lower()
        emoji       = WEATHER_EMOJI.get(condition, "🌡️")
        wind_kph    = round(data["wind"]["speed"] * 3.6)
        tz_offset   = data.get("timezone", 19800)   # default IST = +5:30

        sunrise_str = _fmt_time(data["sys"]["sunrise"], tz_offset)
        sunset_str  = _fmt_time(data["sys"]["sunset"],  tz_offset)

        # ── UV Index (separate endpoint, same key) ────────────────────────
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]
        uv_line = ""
        try:
            uv_resp = requests.get(
                UV_URL,
                params={"lat": lat, "lon": lon, "appid": WEATHER_API_KEY},
                timeout=5,
            )
            if uv_resp.status_code == 200:
                uv_val = uv_resp.json().get("value", None)
                if uv_val is not None:
                    uv_line = f"\n  ☀️ UV Index: {_uv_badge(uv_val)}"
        except Exception:
            pass   # UV is optional; skip silently

        return (
            f"{emoji} *Weather in {city}*\n"
            f"  🌡️ {temp}°C (feels like {feels_like}°C)\n"
            f"  {desc} | 💧 Humidity: {humidity}%\n"
            f"  💨 Wind: {wind_kph} km/h{uv_line}\n"
            f"  🌅 Sunrise: {sunrise_str} · 🌇 Sunset: {sunset_str}"
        )

    except requests.exceptions.ConnectionError:
        log("WEATHER", "Connection error — no internet?")
        return "🌤️ *Weather*\n  Unavailable (no connection)."
    except requests.exceptions.Timeout:
        log("WEATHER", "Request timed out.")
        return "🌤️ *Weather*\n  Unavailable (timeout)."
    except Exception as e:
        log("WEATHER", f"Unexpected error: {e}")
        return f"🌤️ *Weather*\n  Unavailable ({type(e).__name__})."
