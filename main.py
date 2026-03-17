from src.data_loader import fetch_stock_data, fetch_company_info
from src.indicators import add_technical_indicators


def main():
    ticker = "AAPL"

    print(f"\nFetching data for {ticker}...\n")

    stock_data = fetch_stock_data(ticker)
    company_info = fetch_company_info(ticker)

    print("Company Info:")
    print(company_info)

    enriched_data = add_technical_indicators(stock_data)

    print("\nStock Data with Indicators:")
    print(enriched_data[["Close", "SMA_20", "EMA_20", "RSI_14", "MACD", "MACD_Signal", "MACD_Hist"]].tail())


if __name__ == "__main__":
    main()