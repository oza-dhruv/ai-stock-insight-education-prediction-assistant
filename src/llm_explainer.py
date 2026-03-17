import os
import streamlit as st
from openai import OpenAI


def get_openai_api_key():
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return os.getenv("OPENAI_API_KEY")


def generate_llm_explanation(
    ticker,
    company_info,
    signal_summary,
    pred_1d,
    pred_5d,
    sentiment
):
    api_key = get_openai_api_key()

    if not api_key:
        return "AI explanation is unavailable because no OpenAI API key is configured."

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Explain the following stock analysis in simple, beginner-friendly language.

    Ticker: {ticker}
    Company Name: {company_info.get('name', 'N/A')}
    Sector: {company_info.get('sector', 'N/A')}
    Industry: {company_info.get('industry', 'N/A')}

    Bullish Signals: {signal_summary.get('bullish_signals', [])}
    Bearish Signals: {signal_summary.get('bearish_signals', [])}
    Neutral Signals: {signal_summary.get('neutral_signals', [])}

    Next Day Prediction: {pred_1d}
    Next 5 Day Prediction: {pred_5d}

    Sentiment: {sentiment}

    Keep it clear, practical, and easy for a beginner to understand.
    """

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text
    except Exception as e:
        return f"AI explanation is temporarily unavailable: {e}"