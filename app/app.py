import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import streamlit as st

from src.data_loader import fetch_stock_data, fetch_company_info
from src.indicators import (
    add_technical_indicators,
    calculate_bollinger_bands,
    add_volume_features
)
from src.signal_engine import generate_signal_summary
from src.prediction import prepare_prediction_data, train_prediction_model, predict_direction
from src.sentiment import fetch_news_headlines, analyze_sentiment_simple
from src.llm_explainer import generate_llm_explanation
from src.visualization import (
    plot_price_with_moving_averages,
    plot_bollinger_bands,
    plot_rsi,
    plot_macd,
    plot_volume
)

st.set_page_config(page_title="AI Stock Assistant", layout="wide")

st.title("AI Powered Stock Insight, Education, and Prediction Assistant")
st.markdown("---")

ticker = st.text_input("Enter Stock Ticker (e.g., TSLA, AAPL, NVDA):", "TSLA")
analyze = st.button("Analyze Stock")

if analyze:
    stock_data = fetch_stock_data(ticker)

    if stock_data.empty:
        st.warning("Could not load stock data right now. Yahoo Finance may be temporarily rate limiting requests.")
        st.stop()

    company_info = fetch_company_info(ticker)

    enriched_data = add_technical_indicators(stock_data)
    enriched_data = calculate_bollinger_bands(enriched_data)
    enriched_data = add_volume_features(enriched_data)

    # Company Overview
    st.subheader("Company Overview")

    current_price = company_info.get("current_price")
    market_cap = company_info.get("market_cap")
    high_52 = company_info.get("52_week_high")
    low_52 = company_info.get("52_week_low")
    company_name = company_info.get("name") or ticker.upper()
    sector = company_info.get("sector", "N/A")
    industry = company_info.get("industry", "N/A")
    description = company_info.get("description", "No description available.")

    # Fallbacks from stock_data if Yahoo company info is missing
    if current_price is None and not stock_data.empty and "Close" in stock_data.columns:
        current_price = round(float(stock_data["Close"].iloc[-1]), 2)

    if high_52 is None and not stock_data.empty and "High" in stock_data.columns:
        high_52 = round(float(stock_data["High"].max()), 2)

    if low_52 is None and not stock_data.empty and "Low" in stock_data.columns:
        low_52 = round(float(stock_data["Low"].min()), 2)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Current Price", f"${current_price}" if current_price is not None else "N/A")
    col2.metric("Market Cap", f"{market_cap:,}" if market_cap else "N/A")
    col3.metric("52 Week High", f"${high_52}" if high_52 is not None else "N/A")
    col4.metric("52 Week Low", f"${low_52}" if low_52 is not None else "N/A")

    st.write(f"**Company Name:** {company_name}")
    st.write(f"**Sector:** {sector}")
    st.write(f"**Industry:** {industry}")

    with st.expander("Business Description"):
        st.write(description)

    st.markdown("---")

    # Charts
    st.subheader("Charts")

    st.write("Price & Moving Averages")
    st.plotly_chart(plot_price_with_moving_averages(enriched_data, ticker), use_container_width=True)

    st.write("Bollinger Bands")
    st.plotly_chart(plot_bollinger_bands(enriched_data, ticker), use_container_width=True)

    st.write("RSI")
    st.plotly_chart(plot_rsi(enriched_data, ticker), use_container_width=True)

    st.write("MACD")
    st.plotly_chart(plot_macd(enriched_data, ticker), use_container_width=True)

    st.write("Volume")
    st.plotly_chart(plot_volume(enriched_data, ticker), use_container_width=True)

    st.markdown("---")

    # Latest Indicator Values
    st.subheader("Latest Indicator Values")

    latest_row = enriched_data.iloc[-1]

    indicator_df = pd.DataFrame({
        "Indicator": [
            "Close",
            "SMA 20",
            "EMA 20",
            "RSI 14",
            "MACD",
            "MACD Signal",
            "MACD Histogram",
            "Bollinger Upper",
            "Bollinger Middle",
            "Bollinger Lower",
            "Volume",
            "Volume MA 20",
            "Volume Change"
        ],
        "Value": [
            round(latest_row["Close"], 2),
            round(latest_row["SMA_20"], 2),
            round(latest_row["EMA_20"], 2),
            round(latest_row["RSI_14"], 2),
            round(latest_row["MACD"], 2),
            round(latest_row["MACD_Signal"], 2),
            round(latest_row["MACD_Hist"], 2),
            round(latest_row["BB_Upper"], 2),
            round(latest_row["BB_Middle"], 2),
            round(latest_row["BB_Lower"], 2),
            round(latest_row["Volume"], 2),
            round(latest_row["Volume_MA_20"], 2),
            round(latest_row["Volume_Change"], 4)
        ]
    })

    st.dataframe(indicator_df, use_container_width=True)

    st.markdown("---")

    # Historical Data Table
    st.subheader("Recent Historical Market Data")

    historical_df = enriched_data.copy()

    if "Date" not in historical_df.columns:
        historical_df = historical_df.reset_index()

    if "Date" in historical_df.columns:
        historical_df["Date"] = historical_df["Date"].astype(str)

    display_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    available_columns = [col for col in display_columns if col in historical_df.columns]

    st.dataframe(historical_df[available_columns].tail(30), use_container_width=True)

    st.markdown("---")

    # Signals
    signal_summary = generate_signal_summary(enriched_data)

    st.subheader("Signal Summary")

    col1, col2, col3 = st.columns(3)
    col1.metric("Bullish Signals", signal_summary["bullish_count"])
    col2.metric("Bearish Signals", signal_summary["bearish_count"])
    col3.metric("Neutral Signals", signal_summary["neutral_count"])

    with st.expander("Detailed Signals"):
        st.write("**Bullish Signals:**")
        for s in signal_summary["bullish_signals"]:
            st.write(f"- {s}")

        st.write("**Bearish Signals:**")
        for s in signal_summary["bearish_signals"]:
            st.write(f"- {s}")

        st.write("**Neutral Signals:**")
        for s in signal_summary["neutral_signals"]:
            st.write(f"- {s}")

    st.markdown("---")

    # Predictions
    X_1d, y_1d, df_1d = prepare_prediction_data(enriched_data, horizon=1)
    model_1d, acc_1d = train_prediction_model(X_1d, y_1d)
    pred_1d = predict_direction(model_1d, df_1d, "Next Day")

    X_5d, y_5d, df_5d = prepare_prediction_data(enriched_data, horizon=5)
    model_5d, acc_5d = train_prediction_model(X_5d, y_5d)
    pred_5d = predict_direction(model_5d, df_5d, "Next 5 Days")

    st.subheader("Predictions")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Next Day Prediction",
            pred_1d["prediction"],
            f"Up: {pred_1d['probability_up']:.2f}% | Down: {pred_1d['probability_down']:.2f}%"
        )
        st.caption(f"Model Accuracy: {acc_1d:.2%}")

    with col2:
        st.metric(
            "5 Day Prediction",
            pred_5d["prediction"],
            f"Up: {pred_5d['probability_up']:.2f}% | Down: {pred_5d['probability_down']:.2f}%"
        )
        st.caption(f"Model Accuracy: {acc_5d:.2%}")

    st.markdown("---")

    # Sentiment
    headlines = fetch_news_headlines(ticker)
    sentiment = analyze_sentiment_simple(headlines)

    st.subheader("News Sentiment")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall", sentiment["overall_sentiment"])
    col2.metric("Positive", sentiment["positive_count"])
    col3.metric("Negative", sentiment["negative_count"])

    with st.expander("Recent Headlines"):
        for h in headlines[:5]:
            st.write(f"- {h['title']}")

    st.markdown("---")

    # AI Explanation
    st.subheader("AI Explanation")

    explanation = generate_llm_explanation(
        ticker,
        company_info,
        signal_summary,
        pred_1d,
        pred_5d,
        sentiment
    )

    st.write(explanation)