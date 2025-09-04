import pandas as pd
import numpy as np
import plotly.graph_objects as go
from ib_insync import *
from datetime import datetime

# -------------------------------
# 获取数据
# -------------------------------
def fetch_data(symbol="AAPL", exchange="SMART", currency="USD", duration="1 Y", barSize="1 day"):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)
    contract = Stock(symbol, exchange, currency)
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr=duration,
        barSizeSetting=barSize,
        whatToShow='TRADES',
        useRTH=True
    )
    ib.disconnect()
    df = util.df(bars)
    df.set_index("date", inplace=True)
    return df

# -------------------------------
# 策略函数
# -------------------------------
def moving_average_crossover(df, short=10, long=50):
    df = df.copy()
    df['MA_Short'] = df['close'].rolling(short).mean()
    df['MA_Long'] = df['close'].rolling(long).mean()
    df['Signal'] = 0
    df['Signal'][short:] = (df['MA_Short'][short:] > df['MA_Long'][short:]).astype(int)
    df['Position'] = df['Signal'].diff()
    return df

def bollinger_mean_reversion(df, window=20, num_std=2):
    df = df.copy()
    df['MA'] = df['close'].rolling(window).mean()
    df['STD'] = df['close'].rolling(window).std()
    df['Upper'] = df['MA'] + num_std * df['STD']
    df['Lower'] = df['MA'] - num_std * df['STD']
    df['Signal'] = 0
    df.loc[df['close'] < df['Lower'], 'Signal'] = 1
    df.loc[df['close'] > df['Upper'], 'Signal'] = -1
    df['Position'] = df['Signal'].shift()
    return df

def rsi_strategy(df, window=14, lower=30, upper=70):
    df = df.copy()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    RS = gain / loss
    df['RSI'] = 100 - (100 / (1 + RS))
    df['Signal'] = 0
    df.loc[df['RSI'] < lower, 'Signal'] = 1
    df.loc[df['RSI'] > upper, 'Signal'] = -1
    df['Position'] = df['Signal'].shift()
    return df

# -------------------------------
# 回测 + 绩效指标
# -------------------------------
def backtest(df):
    df = df.copy()
    df['Return'] = df['close'].pct_change().fillna(0)
    df['Strategy_Return'] = df['Return'] * df['Position'].shift().fillna(0)
    df['Equity'] = (1 + df['Strategy_Return']).cumprod()

    # 绩效指标
    total_return = df['Equity'].iloc[-1] - 1
    ann_return = df['Strategy_Return'].mean() * 252
    ann_vol = df['Strategy_Return'].std() * np.sqrt(252)
    sharpe = ann_return / ann_vol if ann_vol > 0 else np.nan
    rolling_max = df['Equity'].cummax()
    drawdown = df['Equity'] / rolling_max - 1
    max_dd = drawdown.min()

    trades = df[df['Position'] != 0]
    wins = (df['Strategy_Return'] > 0).sum()
    win_rate = wins / len(trades) if len(trades) > 0 else np.nan

    stats = {
        "Total Return": total_return,
        "Annual Return": ann_return,
        "Volatility": ann_vol,
        "Sharpe": sharpe,
        "Max Drawdown": max_dd,
        "Win Rate": win_rate
    }
    return df['Equity'], stats, df

# -------------------------------
# Plotly 绘图
# -------------------------------
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

def plot_comparison(results):
    fig = go.Figure()
    for name, (equity, stats, df) in results.items():
        fig.add_trace(go.Scatter(x=df.index, y=equity, mode="lines", name=name))
    fig.update_layout(title="Strategy Comparison (Cumulative Returns)", xaxis_title="Date", yaxis_title="Equity")
    fig.show()

# -------------------------------
# 主程序
# -------------------------------
if __name__ == "__main__":
    df = fetch_data("AAPL", duration="1 Y")

    strategies = {
        "MA Crossover": moving_average_crossover(df),
        "Bollinger": bollinger_mean_reversion(df),
        "RSI": rsi_strategy(df)
    }

    results = {}
    for name, strat_df in strategies.items():
        equity, stats, detailed_df = backtest(strat_df)
        results[name] = (equity, stats, detailed_df)

    # 绘制收益曲线对比
    plot_comparison(results)

    # 绘制每个策略的交易信号
    for name, (equity, stats, strat_df) in results.items():
        plot_strategy(strat_df, name)

    # 输出绩效指标表格
    stats_df = pd.DataFrame({name: stats for name, (eq, stats, df) in results.items()}).T
    print("\n=== Performance Metrics ===")
    print(stats_df.round(3))
