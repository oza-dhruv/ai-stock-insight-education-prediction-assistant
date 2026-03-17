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

def calculate_bollinger_bands(data, window=20):
    """
    Calculate Bollinger Bands (Upper, Middle, Lower)
    """

    df = data.copy()

    df["BB_Middle"] = df["Close"].rolling(window=window).mean()
    df["BB_Std"] = df["Close"].rolling(window=window).std()

    df["BB_Upper"] = df["BB_Middle"] + (2 * df["BB_Std"])
    df["BB_Lower"] = df["BB_Middle"] - (2 * df["BB_Std"])

    return df

def add_volume_features(data):
    """
    Add volume-based indicators
    """

    df = data.copy()

    df["Volume_MA_20"] = df["Volume"].rolling(window=20).mean()
    df["Volume_Change"] = df["Volume"].pct_change()

    return df



