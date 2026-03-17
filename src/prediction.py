import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def prepare_prediction_data(data):
    """
    Prepare features and target for next-day direction prediction.
    """

    df = data.copy()

    # Daily return
    df["Return"] = df["Close"].pct_change()

    # Target: 1 if next day's close is higher, else 0
    df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

    # Drop rows with missing values
    df = df.dropna()

    features = ["Close", "Volume", "SMA_20", "EMA_20", "RSI_14", "MACD", "MACD_Signal", "MACD_Hist", "Return"]
    X = df[features]
    y = df["Target"]

    return X, y, df


def train_prediction_model(X, y):
    """
    Train a Random Forest model and return the trained model and accuracy.
    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    return model, accuracy


def predict_next_day_direction(model, df):
    """
    Predict the next day's direction using the latest available row.
    """

    latest_features = df[["Close", "Volume", "SMA_20", "EMA_20", "RSI_14", "MACD", "MACD_Signal", "MACD_Hist", "Return"]].iloc[[-1]]
    prediction = model.predict(latest_features)[0]
    probabilities = model.predict_proba(latest_features)[0]

    return {
        "prediction": "Bullish" if prediction == 1 else "Bearish",
        "probability_down": round(probabilities[0] * 100, 2),
        "probability_up": round(probabilities[1] * 100, 2)
    }