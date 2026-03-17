from src.data_loader import fetch_stock_data, fetch_company_info
from src.indicators import (
    add_technical_indicators,
    calculate_bollinger_bands,
    add_volume_features
)
from src.signal_engine import generate_signal_summary
from src.visualization import plot_price_with_moving_averages, plot_bollinger_bands
from src.prediction import prepare_prediction_data, train_prediction_model, predict_direction
from src.sentiment import fetch_news_headlines, analyze_sentiment_simple



def main():
    ticker = "TSLA"

    print(f"\nFetching data for {ticker}...\n")

    stock_data = fetch_stock_data(ticker)
    company_info = fetch_company_info(ticker)

    print("Company Info:")
    print(company_info)

    enriched_data = add_technical_indicators(stock_data)
    enriched_data = calculate_bollinger_bands(enriched_data)
    enriched_data = add_volume_features(enriched_data)  

    print("\nStock Data with Indicators:")
    print(
    enriched_data[
        [
            "Close",
            "SMA_20",
            "EMA_20",
            "RSI_14",
            "MACD",
            "MACD_Signal",
            "MACD_Hist",
            "BB_Middle",
            "BB_Upper",
            "BB_Lower",
            "Volume_MA_20",
            "Volume_Change"
        ]
    ].tail()
    )

    signal_summary = generate_signal_summary(enriched_data)

    print("\nSignal Summary:")
    print(signal_summary)
    plot_price_with_moving_averages(enriched_data, ticker)
    plot_bollinger_bands(enriched_data, ticker)

    # Next-day prediction
    X_1d, y_1d, prediction_df_1d = prepare_prediction_data(enriched_data, horizon=1)
    model_1d, accuracy_1d = train_prediction_model(X_1d, y_1d)
    next_day_prediction = predict_direction(model_1d, prediction_df_1d, horizon_label="Next Day")

    print("\nNext-Day Model Accuracy:")
    print(f"{accuracy_1d:.2%}")

    print("\nNext-Day Prediction:")
    print(next_day_prediction)

    # 5-day prediction
    X_5d, y_5d, prediction_df_5d = prepare_prediction_data(enriched_data, horizon=5)
    model_5d, accuracy_5d = train_prediction_model(X_5d, y_5d)
    next_5_day_prediction = predict_direction(model_5d, prediction_df_5d, horizon_label="Next 5 Days")

    print("\n5-Day Model Accuracy:")
    print(f"{accuracy_5d:.2%}")

    print("\n5-Day Prediction:")
    print(next_5_day_prediction)

    news_headlines = fetch_news_headlines(ticker, page_size=10)
    sentiment_summary = analyze_sentiment_simple(news_headlines)

    print("\nRecent News Headlines:")
    for item in news_headlines[:5]:
        print(f"- {item['title']} ({item['source']})")

    print("\nSentiment Summary:")
    print(sentiment_summary)

if __name__ == "__main__":
    main()