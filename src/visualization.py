import plotly.graph_objects as go


def plot_price_with_moving_averages(data, ticker):
    """
    Plot stock price with SMA and EMA.
    """

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["SMA_20"],
            mode="lines",
            name="SMA 20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["EMA_20"],
            mode="lines",
            name="EMA 20"
        )
    )

    fig.update_layout(
        title=f"{ticker} Price with Moving Averages",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark"
    )

    fig.show()

def plot_bollinger_bands(data, ticker):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["BB_Upper"],
            mode="lines",
            name="BB Upper"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["BB_Middle"],
            mode="lines",
            name="BB Middle"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["BB_Lower"],
            mode="lines",
            name="BB Lower"
        )
    )

    fig.update_layout(
        title=f"{ticker} Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    fig.show()