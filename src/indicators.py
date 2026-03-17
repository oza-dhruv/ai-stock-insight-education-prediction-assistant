import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator


def add_technical_indicators(data):
    """
    Add technical indicators to stock price data.

    Parameters:
        data (pd.DataFrame): Historical stock data

    Returns:
        pd.DataFrame: Data with technical indicators added
    """

    df = data.copy()

    # Simple Moving Average (20-day)
    df["SMA_20"] = SMAIndicator(close=df["Close"], window=20).sma_indicator()

    # Exponential Moving Average (20-day)
    df["EMA_20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()

    # Relative Strength Index (14-day)
    df["RSI_14"] = RSIIndicator(close=df["Close"], window=14).rsi()

    # MACD
    macd = MACD(close=df["Close"])
    df["MACD"] = macd.macd()
    df["MACD_Signal"] = macd.macd_signal()
    df["MACD_Hist"] = macd.macd_diff()

    return df