import pandas as pd


def compute_vwap(df: pd.DataFrame) -> pd.Series:
    return df["quote_asset_volume"] / df["volume"]


def compute_relative_volatility(df: pd.DataFrame, price_col: str = "vwap") -> pd.Series:
    return (df["high"] - df["low"]) / df[price_col]


def compute_volume_baseline(df: pd.DataFrame, window: int = 30) -> pd.Series:
    return df["volume"].rolling(window).mean()


def add_market_features(df: pd.DataFrame) -> pd.DataFrame:

    df["vwap"] = compute_vwap(df)
    df["relative_volatility"] = compute_relative_volatility(df, price_col="vwap")
    df["volume_baseline"] = compute_volume_baseline(df)

    return df