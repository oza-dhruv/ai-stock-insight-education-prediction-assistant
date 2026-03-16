import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period="1y"):
    """
    Fetch historical stock data for a given ticker.

    Parameters:
        ticker (str): Stock ticker symbol (e.g., AAPL)
        period (str): Time range of data (e.g., 1y, 6mo, 3mo)

    Returns:
        pandas.DataFrame: Stock price data
    """

    stock = yf.Ticker(ticker)

    data = stock.history(period=period)

    return data


def fetch_company_info(ticker):
    """
    Fetch basic company information.

    Parameters:
        ticker (str): Stock ticker symbol

    Returns:
        dict: Company information
    """

    stock = yf.Ticker(ticker)

    info = stock.info

    company_data = {
        "name": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "market_cap": info.get("marketCap"),
        "current_price": info.get("currentPrice"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "description": info.get("longBusinessSummary")
    }

    return company_data