import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


FEATURE_COLUMNS = [
    "Close",
    "Volume",
    "SMA_20",
    "EMA_20",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "Return_1D",
    "Return_5D",
    "Volatility_5D",
    "Price_vs_SMA20",
    "Price_vs_EMA20",
    "Volume_Change"
]


def add_prediction_features(data):
    """
    Add extra model features to improve prediction quality.
    """

    df = data.copy()

    df["Return_1D"] = df["Close"].pct_change()
    df["Return_5D"] = df["Close"].pct_change(periods=5)
    df["Volatility_5D"] = df["Return_1D"].rolling(window=5).std()
    df["Price_vs_SMA20"] = (df["Close"] - df["SMA_20"]) / df["SMA_20"]
    df["Price_vs_EMA20"] = (df["Close"] - df["EMA_20"]) / df["EMA_20"]
    df["Volume_Change"] = df["Volume"].pct_change()

    return df


def prepare_prediction_data(data, horizon=1):
    """
    Prepare features and target for stock direction prediction.

    horizon=1  -> next day direction
    horizon=5  -> next 5 day direction
    """

    df = add_prediction_features(data)

    df["Target"] = (df["Close"].shift(-horizon) > df["Close"]).astype(int)

    df = df.dropna()

    X = df[FEATURE_COLUMNS]
    y = df["Target"]

    return X, y, df


def train_prediction_model(X, y):
    """
    Train a Random Forest model and return the trained model and accuracy.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy


def predict_direction(model, df, horizon_label="Next Day"):
    """
    Predict stock direction using the latest available row.
    """

    latest_features = df[FEATURE_COLUMNS].iloc[[-1]]
    prediction = model.predict(latest_features)[0]
    probabilities = model.predict_proba(latest_features)[0]

    return {
        "horizon": horizon_label,
        "prediction": "Bullish" if prediction == 1 else "Bearish",
        "probability_down": float(round(probabilities[0] * 100, 2)),
        "probability_up": float(round(probabilities[1] * 100, 2))
    }