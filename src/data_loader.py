import time
import pandas as pd
import yfinance as yf
import streamlit as st


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_stock_data(ticker, period="6mo"):
    ticker = ticker.strip().upper()

    for attempt in range(3):
        try:
            data = yf.download(
                ticker,
                period=period,
                progress=False,
                auto_adjust=False,
                threads=False
            )

            if data is None or data.empty:
                return pd.DataFrame()

            # Flatten MultiIndex columns if Yahoo returns them
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = [col[0] for col in data.columns]

            data = data.reset_index()

            # Keep only the columns the app needs
            expected_cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
            available_cols = [col for col in expected_cols if col in data.columns]
            data = data[available_cols].copy()

            # Make sure numeric columns are numeric
            for col in ["Open", "High", "Low", "Close", "Volume"]:
                if col in data.columns:
                    data[col] = pd.to_numeric(data[col], errors="coerce")

            # Drop rows where Close is missing
            if "Close" in data.columns:
                data = data.dropna(subset=["Close"])

            return data

        except Exception as e:
            error_name = type(e).__name__

            if "YFRateLimitError" in error_name or "rate" in str(e).lower():
                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue
                return pd.DataFrame()

            return pd.DataFrame()

    return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_company_info(ticker):
    ticker = ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info:
            return {}

        return {
            "name": info.get("longName") or info.get("shortName") or ticker,
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "description": info.get("longBusinessSummary", "No description available."),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "market_cap": info.get("marketCap"),
            "52_week_high": info.get("fiftyTwoWeekHigh"),
            "52_week_low": info.get("fiftyTwoWeekLow"),
        }

    except Exception:
        return {}