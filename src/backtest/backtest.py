import numpy as np

def backtest(df):
    df = df.copy()
    df['Return'] = df['close'].pct_change().fillna(0)
    df['Strategy_Return'] = df['Return'] * df['Position'].shift().fillna(0)
    df['Equity'] = (1 + df['Strategy_Return']).cumprod()

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