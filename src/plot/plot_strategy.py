import plotly.graph_objects as go

def plot_strategy(df, name="Strategy"):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], mode='lines', name="Price"))
    buys = df[df['Position'] == 1]
    fig.add_trace(go.Scatter(x=buys.index, y=buys['close'], mode="markers", name="Buy",
                             marker=dict(color="green", size=10, symbol="triangle-up")))
    sells = df[df['Position'] == -1]
    fig.add_trace(go.Scatter(x=sells.index, y=sells['close'], mode="markers", name="Sell",
                             marker=dict(color="red", size=10, symbol="triangle-down")))
    fig.update_layout(title=f"{name} Trading Signals", xaxis_title="Date", yaxis_title="Price")
    fig.show()