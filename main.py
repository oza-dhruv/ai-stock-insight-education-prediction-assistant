from src.data_loader import fetch_stock_data, fetch_company_info
from src.indicators import add_technical_indicators
from src.signal_engine import generate_signal_summary
from src.visualization import plot_price_with_moving_averages
from src.prediction import prepare_prediction_data, train_prediction_model, predict_next_day_direction

def main():
    ticker = "NVDA"

    print(f"\nFetching data for {ticker}...\n")

    stock_data = fetch_stock_data(ticker)
    company_info = fetch_company_info(ticker)

    print("Company Info:")
    print(company_info)

    enriched_data = add_technical_indicators(stock_data)

    print("\nStock Data with Indicators:")
    print(enriched_data[["Close", "SMA_20", "EMA_20", "RSI_14", "MACD", "MACD_Signal", "MACD_Hist"]].tail())

    signal_summary = generate_signal_summary(enriched_data)

    print("\nSignal Summary:")
    print(signal_summary)
    plot_price_with_moving_averages(enriched_data, ticker)

    X, y, prediction_df = prepare_prediction_data(enriched_data)
    model, accuracy = train_prediction_model(X, y)
    next_day_prediction = predict_next_day_direction(model, prediction_df)

    print("\nModel Accuracy:")
    print(f"{accuracy:.2%}")

    print("\nNext Day Prediction:")
    print(next_day_prediction)

if __name__ == "__main__":
    main()