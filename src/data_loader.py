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

            data = data.reset_index()
            return data

        except Exception as e:
            error_name = type(e).__name__

            if "YFRateLimitError" in error_name or "rate" in str(e).lower():
                if attempt < 2:
                    time.sleep(3 * (attempt + 1))
                    continue
                return pd.DataFrame()

            return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_company_info(ticker):
    ticker = ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return info if info else {}
    except Exception:
        return {}