"""
crypto.py — Live markets & crypto price snapshot.
Uses CoinGecko API for Crypto, Yahoo Finance for Indian Markets (free, no keys).
Shows metrics with 24-hour change and trend emoji.
"""

import requests
from src.logger import log


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1d&interval=1d"

COINS = {
    "bitcoin":  ("BTC", "₿"),
    "ethereum": ("ETH", "Ξ"),
}

MARKETS = {
    "^NSEI":  ("NIFTY", "📊"),
    "^BSESN": ("SENSEX", "📈"),
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
    Returns a formatted markets & crypto price block.
    Falls back gracefully if APIs are unreachable.
    """
    lines = []

    # 1. Market Data (Yahoo Finance)
    for symbol, (name, icon) in MARKETS.items():
        try:
            resp = requests.get(
                YAHOO_URL.format(symbol=symbol),
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            if resp.status_code == 200:
                meta = resp.json()["chart"]["result"][0]["meta"]
                current = meta.get("regularMarketPrice", 0)
                prev = meta.get("chartPreviousClose", 0)
                if current and prev:
                    change_pct = ((current - prev) / prev) * 100
                    trend = _trend_emoji(change_pct)
                    sign = "+" if change_pct >= 0 else ""
                    lines.append(f"  {icon} *{name}*: {current:,.0f}  {trend} {sign}{change_pct:.2f}%")
        except Exception as e:
            log("CRYPTO", f"Market data failed for {symbol}: {e}")

    # 2. Crypto Data (CoinGecko)
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
        if resp.status_code == 200:
            data = resp.json()
            for coin_id, (sym, icon) in COINS.items():
                if coin_id not in data:
                    continue
                price_inr = data[coin_id].get("inr", 0)
                change_24h = data[coin_id].get("inr_24h_change", 0.0)
                trend = _trend_emoji(change_24h)
                sign  = "+" if change_24h >= 0 else ""
                price_fmt = f"₹{price_inr:,.0f}"
                lines.append(
                    f"  {icon} *{sym}*: {price_fmt}  {trend} {sign}{change_24h:.2f}%"
                )
    except Exception as e:
        log("CRYPTO", f"Crypto data failed: {e}")

    if not lines:
        return ""

    return "💰 *Markets & Crypto Snapshot*\n" + "\n".join(lines)
