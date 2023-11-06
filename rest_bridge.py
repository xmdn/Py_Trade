import requests

BINANCE_API_URL = "https://api.binance.com/api/v3/klines"


def fetch_binance_klines(symbol: str, interval: str, startTime: int, endTime: int):
    params = {
        "symbol": symbol,          # e.g., "BTCUSDT"
        "interval": interval,      # Candlestick interval, e.g., "1m", "5m", "1d"
        "startTime": startTime,    # Start time in milliseconds
        "endTime": endTime         # End time in milliseconds
    }

    response = requests.get(BINANCE_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
