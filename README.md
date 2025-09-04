# IBKR Strategy Project

This project implements various trading strategies using the Interactive Brokers API to fetch historical stock data and backtest different trading strategies.

## Project Structure

```
ibkr-strategy-project
├── src
│   ├── __init__.py
│   ├── data
│   │   └── fetch_data.py
│   ├── strategies
│   │   ├── __init__.py
│   │   ├── moving_average_crossover.py
│   │   ├── bollinger_mean_reversion.py
│   │   └── rsi_strategy.py
│   ├── backtest
│   │   └── backtest.py
│   ├── plot
│   │   ├── plot_strategy.py
│   │   └── plot_comparison.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Installation

To set up the project, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd ibkr-strategy-project
pip install -r requirements.txt
```

## Usage

1. **Fetch Data**: Use the `fetch_data` function from `src/data/fetch_data.py` to retrieve historical stock data from the IBKR API.

2. **Select Strategy**: Choose from the following strategies implemented in the `src/strategies` directory:
   - **Moving Average Crossover**: Implemented in `moving_average_crossover.py`.
   - **Bollinger Bands Mean Reversion**: Implemented in `bollinger_mean_reversion.py`.
   - **RSI Strategy**: Implemented in `rsi_strategy.py`.

3. **Backtesting**: The `backtest` function in `src/backtest/backtest.py` can be used to evaluate the performance of the selected strategy.

4. **Visualization**: Use the plotting functions in `src/plot` to visualize the trading signals and compare the performance of different strategies.

## Example

To run the main application, execute the following command:

```bash
python src/main.py
```

This will fetch the stock data, apply the selected trading strategies, run backtests, and generate performance plots.

## Requirements

The project requires the following Python packages:

- pandas
- numpy
- plotly
- ib_insync

Make sure to install these packages using the `requirements.txt` file provided.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.