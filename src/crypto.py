"""
crypto.py — Live crypto price snapshot.
Uses CoinGecko public API — completely free, no API key required.
Shows BTC, ETH with 24-hour change and trend emoji.
"""

import requests
from src.logger import log


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

COINS = {
    "bitcoin":  ("BTC", "₿"),
    "ethereum": ("ETH", "Ξ"),
}


def _trend_emoji(change: float) -> str:
    if change >= 3:
        return "🚀"
    elif change >= 1:
        return "📈"
    elif change >= -1:
        return "➡️"
    elif change >= -3:
        return "📉"
    else:
        return "🔻"


def get_crypto_snapshot() -> str:
    """
    Returns a formatted crypto price block.
    Falls back gracefully if CoinGecko is unreachable.
    """
    try:
        resp = requests.get(
            COINGECKO_URL,
            params={
                "ids":            ",".join(COINS.keys()),
                "vs_currencies":  "inr",
                "include_24hr_change": "true",
            },
            timeout=8,
            headers={"User-Agent": "MorningBriefingBot/2.0"},
        )
        resp.raise_for_status()
        data = resp.json()

        lines = []
        for coin_id, (symbol, icon) in COINS.items():
            if coin_id not in data:
                continue
            price_inr = data[coin_id].get("inr", 0)
            change_24h = data[coin_id].get("inr_24h_change", 0.0)
            trend = _trend_emoji(change_24h)
            sign  = "+" if change_24h >= 0 else ""
            price_fmt = f"₹{price_inr:,.0f}"
            lines.append(
                f"  {icon} *{symbol}*: {price_fmt}  {trend} {sign}{change_24h:.1f}%"
            )

        if not lines:
            return ""

        log("CRYPTO", f"Fetched prices for {', '.join(COINS.keys())}")
        return "💰 *Crypto Snapshot* _(24h change)_\n" + "\n".join(lines)

    except requests.exceptions.ConnectionError:
        log("CRYPTO", "No internet — skipping crypto snapshot.")
        return ""
    except Exception as e:
        log("CRYPTO", f"Failed: {e}")
        return ""
