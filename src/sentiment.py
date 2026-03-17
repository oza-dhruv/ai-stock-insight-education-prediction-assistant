import os
import requests
from dotenv import load_dotenv


load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")


def fetch_news_headlines(query, page_size=10):
    """
    Fetch recent news headlines for a stock or company using NewsAPI.
    """

    if not NEWS_API_KEY:
        raise ValueError("NEWS_API_KEY not found in environment variables.")

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise ValueError(f"NewsAPI error: {data}")

    articles = data.get("articles", [])

    headlines = []
    for article in articles:
        title = article.get("title")
        source = article.get("source", {}).get("name")
        published_at = article.get("publishedAt")

        if title:
            headlines.append({
                "title": title,
                "source": source,
                "published_at": published_at
            })

    return headlines


def analyze_sentiment_simple(headlines):
    """
    Very simple rule-based sentiment analysis using keyword matching.
    """

    positive_keywords = [
        "gain", "gains", "up", "surge", "surges", "beat", "beats",
        "growth", "strong", "record", "bullish", "upgrade", "profit"
    ]

    negative_keywords = [
        "fall", "falls", "down", "drop", "drops", "miss", "misses",
        "weak", "loss", "bearish", "downgrade", "decline", "risk"
    ]

    positive_count = 0
    negative_count = 0
    neutral_count = 0

    for item in headlines:
        title = item["title"].lower()

        positive_matches = sum(word in title for word in positive_keywords)
        negative_matches = sum(word in title for word in negative_keywords)

        if positive_matches > negative_matches:
            positive_count += 1
        elif negative_matches > positive_matches:
            negative_count += 1
        else:
            neutral_count += 1

    if positive_count > negative_count:
        overall_sentiment = "Positive"
    elif negative_count > positive_count:
        overall_sentiment = "Negative"
    else:
        overall_sentiment = "Neutral"

    return {
        "overall_sentiment": overall_sentiment,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "headline_count": len(headlines)
    }