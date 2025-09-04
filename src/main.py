import pandas as pd
from data.fetch_data import fetch_data
from strategies.moving_average_crossover import moving_average_crossover
from strategies.bollinger_mean_reversion import bollinger_mean_reversion
from strategies.rsi_strategy import rsi_strategy
from backtest.backtest import backtest
from plot.plot_strategy import plot_strategy
from plot.plot_comparison import plot_comparison

if __name__ == "__main__":
    symbol = "AAPL"
    duration = "1 Y"

    df = fetch_data(symbol, duration=duration)

    strategies = {
        "MA Crossover": moving_average_crossover(df),
        "Bollinger": bollinger_mean_reversion(df),
        "RSI": rsi_strategy(df)
    }

    results = {}
    for name, strat_df in strategies.items():
        equity, stats, detailed_df = backtest(strat_df)
        results[name] = (equity, stats, detailed_df)

    plot_comparison(results)

    for name, (equity, stats, strat_df) in results.items():
        plot_strategy(strat_df, name)

    stats_df = pd.DataFrame({name: stats for name, (eq, stats, df) in results.items()}).T
    print("\n=== Performance Metrics ===")
    print(stats_df.round(3))