from enum import Enum


class BinanceConfig:
    BASE_URL = "https://api.binance.com"
    TIMEOUT = 10  # Seconds to wait before giving up on a request
    MAX_RETRIES = 3


class PublicEndpoints(Enum):
    KLINES = "/api/v3/klines"
    TRADES = "/api/v3/trades"
