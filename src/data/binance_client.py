import requests
import pandas as pd
from datetime import datetime
from src.data.constants import BinanceConfig, PublicEndpoints   


class BinanceClient:
    def __init__(self):
        self.base_url = BinanceConfig.BASE_URL

    def _get(self, endpoint: str, params: dict = None):
        """Generic GET request handler"""
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} - {response.text}")

        return response.json()

    def get_klines(
        self,
        symbol: str = "BTCUSDT",
        interval: str = "1d",
        start_time: int = None,
        end_time: int = None,
        limit: int = 365,
    ) -> pd.DataFrame:
        """
        Fetch kline (candlestick) data and return as DataFrame.

        Parameters:
        - symbol: trading pair (e.g., BTCUSDT)
        - interval: kline interval (e.g., 1m, 1h, 1d)
        - start_time: in milliseconds
        - end_time: in milliseconds
        - limit: max number of rows (<=1000)
        """

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit,
        }

        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        data = self._get(PublicEndpoints.KLINES.value, params=params)

        columns = [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ]

        df = pd.DataFrame(data, columns=columns)

        # Convert numeric columns
        numeric_cols = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_asset_volume",
            "taker_buy_base",
            "taker_buy_quote",
        ]
        df[numeric_cols] = df[numeric_cols].astype(float)

        # Convert timestamps
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

        return df

    def get_recent_trades(self, symbol: str = "BTCUSDT", limit: int = 500):
        """
        Fetch recent trades (tick-level data).
        """
        params = {"symbol": symbol, "limit": limit}
        return self._get(PublicEndpoints.TRADES.value, params=params)


# --- Utility functions ---

def datetime_to_milliseconds(dt: datetime) -> int:
    """Convert datetime to Binance timestamp (ms)"""
    return int(dt.timestamp() * 1000)
