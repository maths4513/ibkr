import pandas as pd
from data.fetch_data import fetch_data
from strategies.rsi_strategy import rsi_strategy
from strategies.moving_average_crossover import moving_average_crossover
from strategies.bollinger_mean_reversion import bollinger_mean_reversion
from backtest.backtest import backtest
from plot.plot_strategy import plot_strategy
from plot.plot_comparison import plot_comparison

if __name__ == "__main__":
    symbols = ["IBKR", "GOOG", "JD", "PLTR"]  # 你可以自定义股票列表
    duration = "1 Y"

    results = {}
    for symbol in symbols:
        df = fetch_data(symbol, duration=duration)
        #strat_df = rsi_strategy(df)
        #strat_df = moving_average_crossover(df)
        strat_df = bollinger_mean_reversion(df)
        equity, stats, detailed_df = backtest(strat_df)
        results[symbol] = (equity, stats, detailed_df)

    plot_comparison(results)

    for symbol, (equity, stats, strat_df) in results.items():
        plot_strategy(strat_df, symbol)

    stats_df = pd.DataFrame({symbol: stats for symbol, (eq, stats, df) in results.items()}).T
    print("\n=== RSI策略在不同股票下的绩效 ===")
    print(stats_df.round(3))