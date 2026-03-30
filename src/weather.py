"""
weather.py — Fetches current weather from OpenWeatherMap (free tier).
Endpoint: api.openweathermap.org/data/2.5/weather
"""

import requests
from src.config import WEATHER_API_KEY, WEATHER_CITY
from src.logger import log


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

WEATHER_EMOJI = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "haze": "🌫️",
    "fog": "🌫️",
    "smoke": "💨",
}


def get_weather(city: str = WEATHER_CITY) -> str:
    """
    Returns a formatted weather string for the given city.
    Falls back gracefully on any error.
    """
    if not WEATHER_API_KEY:
        return "🌤️ Weather: API key not set."

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

        temp       = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        humidity   = data["main"]["humidity"]
        desc       = data["weather"][0]["description"].capitalize()
        condition  = data["weather"][0]["main"].lower()
        emoji      = WEATHER_EMOJI.get(condition, "🌡️")
        wind_kph   = round(data["wind"]["speed"] * 3.6)

        return (
            f"{emoji} *Weather in {city}*\n"
            f"  Temp: {temp}°C (feels like {feels_like}°C)\n"
            f"  {desc} | Humidity: {humidity}%\n"
            f"  Wind: {wind_kph} km/h"
        )

    except requests.exceptions.ConnectionError:
        log("WEATHER", "Connection error — no internet?")
        return "🌤️ Weather unavailable (no connection)."
    except requests.exceptions.Timeout:
        log("WEATHER", "Request timed out.")
        return "🌤️ Weather unavailable (timeout)."
    except Exception as e:
        log("WEATHER", f"Unexpected error: {e}")
        return f"🌤️ Weather unavailable ({type(e).__name__})."
