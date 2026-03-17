import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_llm_explanation(
    ticker,
    company_info,
    signal_summary,
    next_day_prediction,
    next_5_day_prediction,
    sentiment_summary
):
    """
    Generate a beginner-friendly explanation of stock insights.
    """

    prompt = f"""
You are a beginner-friendly stock education assistant.

Explain everything in simple language for a student or early investor.
Do not give financial advice.
Do not tell the user to buy, sell, or hold.
Only explain what the data suggests.

Stock ticker: {ticker}

Company Information:
- Name: {company_info.get("name")}
- Sector: {company_info.get("sector")}
- Industry: {company_info.get("industry")}
- Current Price: {company_info.get("current_price")}
- 52 Week High: {company_info.get("52_week_high")}
- 52 Week Low: {company_info.get("52_week_low")}

Signal Summary:
- Bullish signals: {signal_summary.get("bullish_count")}
- Bearish signals: {signal_summary.get("bearish_count")}
- Neutral signals: {signal_summary.get("neutral_count")}
- Bullish details: {signal_summary.get("bullish_signals")}
- Bearish details: {signal_summary.get("bearish_signals")}
- Neutral details: {signal_summary.get("neutral_signals")}

Prediction Summary:
- Next Day: {next_day_prediction}
- Next 5 Days: {next_5_day_prediction}

Sentiment Summary:
- Overall Sentiment: {sentiment_summary.get("overall_sentiment")}
- Positive Headlines: {sentiment_summary.get("positive_count")}
- Negative Headlines: {sentiment_summary.get("negative_count")}
- Neutral Headlines: {sentiment_summary.get("neutral_count")}

Write the response with these sections:
1. Company overview
2. What the indicators suggest
3. What the predictions suggest
4. What the sentiment suggests
5. Final beginner-friendly summary
6. A reminder that this is not financial advice
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text