def generate_signal_summary(data):
    """
    Generate a bullish/bearish signal summary based on the latest indicator values.

    Parameters:
        data (pd.DataFrame): Stock data with technical indicators

    Returns:
        dict: Signal counts and explanations
    """

    latest = data.iloc[-1]

    bullish_signals = []
    bearish_signals = []
    neutral_signals = []

    # Price vs SMA 20
    if latest["Close"] > latest["SMA_20"]:
        bullish_signals.append("Price is above SMA 20, which may indicate short-term upward momentum.")
    else:
        bearish_signals.append("Price is below SMA 20, which may indicate short-term weakness.")

    # Price vs EMA 20
    if latest["Close"] > latest["EMA_20"]:
        bullish_signals.append("Price is above EMA 20, suggesting recent strength.")
    else:
        bearish_signals.append("Price is below EMA 20, suggesting recent weakness.")

    # RSI
    if latest["RSI_14"] > 70:
        neutral_signals.append("RSI is above 70, which can indicate overbought conditions.")
    elif latest["RSI_14"] < 30:
        neutral_signals.append("RSI is below 30, which can indicate oversold conditions.")
    else:
        neutral_signals.append("RSI is in a moderate range, suggesting balanced momentum.")

    # MACD vs Signal
    if latest["MACD"] > latest["MACD_Signal"]:
        bullish_signals.append("MACD is above the signal line, which may indicate bullish momentum.")
    else:
        bearish_signals.append("MACD is below the signal line, which may indicate bearish momentum.")

    return {
        "bullish_count": len(bullish_signals),
        "bearish_count": len(bearish_signals),
        "neutral_count": len(neutral_signals),
        "bullish_signals": bullish_signals,
        "bearish_signals": bearish_signals,
        "neutral_signals": neutral_signals
    }