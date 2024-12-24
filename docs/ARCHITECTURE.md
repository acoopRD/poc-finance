# Kraken Futures Trading Analysis System

## System Overview
A Python-based system for analyzing cryptocurrency futures markets on Kraken, providing technical analysis and market insights.

## Core Components

### 1. Client Management (`kraken_client_factory.py`)
- **Purpose**: Creates authenticated clients for Kraken Futures API.
- **Functions**:
  - `create_futures_client(key_file='kraken.key')`: Reads API keys from a file and creates a client instance.

### 2. Symbol Configuration (`config/symbols.py`)
- **Purpose**: Defines supported trading pairs and their specific parameters.
- **Functions**:
  - `get_symbol_config(symbol: str) -> dict`: Retrieves configuration for a given symbol.
- **Supported Symbols**:
  - BTC: Bitcoin
  - ETH: Ethereum
  - SOL: Solana
  - (Add more symbols as needed)

### 3. Market Data Analysis (`analysis/market_data.py`)
- **Purpose**: Fetches and processes market data for analysis.
- **Functions**:
  - `get_market_data(client, symbol: str) -> Dict`: Fetches comprehensive market data for a symbol.
  - `get_historical_data(client, symbol: str) -> List[float]`: Retrieves and processes historical price data.
  - `analyze_orderbook(orderbook: Dict) -> Dict`: Analyzes order book for market sentiment.
  - `analyze_liquidity(orderbook: Dict) -> Dict`: Analyzes market liquidity.
  - `process_historical_prices(historical_data: List) -> List[float]`: Processes historical price data into a clean list.

### 4. Technical Analysis (`analysis/technical.py`)
- **Purpose**: Calculates technical indicators for market analysis.
- **Functions**:
  - `calculate_rsi(prices: List[float], periods: int = 14) -> float`: Calculates the Relative Strength Index.
  - `calculate_macd(prices: List[float]) -> Dict`: Calculates the MACD (Moving Average Convergence Divergence).
  - `calculate_volatility(prices: List[float]) -> Dict`: Calculates volatility metrics.
  - `detect_trend(prices: List[float]) -> Dict`: Detects price trend and strength.
  - `calculate_bollinger_bands(prices: List[float], periods: int = 20, num_std_dev: int = 2) -> Dict`: Calculates Bollinger Bands.
  - `calculate_moving_average(prices: List[float], periods: int = 50) -> float`: Calculates Simple Moving Average.
  - `detect_abcde_pattern(prices: List[float]) -> bool`: Detects a hypothetical ABCDE pattern in the price list.

### 5. Trading Signals (`analysis/signals.py`)
- **Purpose**: Generates trading signals based on technical indicators.
- **Functions**:
  - `analyze_technical_signals(technical_data: Dict) -> List[Tuple[str, str, int]]`: Analyzes technical indicators for trading signals.
  - `get_trading_recommendation(technical_data: Dict, ticker: Dict) -> Dict`: Generates trading recommendations based on technical indicators.

### 6. Advanced Trading Strategies (`analysis/strategies.py`)
- **Purpose**: Implements advanced trading strategies.
- **Functions**:
  - `bollinger_band_strategy(technical_data: Dict) -> str`: Bollinger Band trading strategy.
  - `moving_average_crossover_strategy(technical_data: Dict) -> str`: Moving Average Crossover trading strategy.

### 7. LLM Data Formatter (`analysis/llm_formatter.py`)
- **Purpose**: Formats market analysis data for consumption by a language model (LLM).
- **Functions**:
  - `format_llm_analysis(market_data: Dict, symbol_config: Dict) -> Dict`: Formats comprehensive market analysis for LLM consumption.

### 8. News and Sentiment Analysis (`analysis/news.py`)
- **Purpose**: Fetches and analyzes news articles for sentiment analysis.
- **Functions**:
  - `fetch_news(symbol: str) -> List[Dict]`: Fetches latest news articles related to the given symbol.
  - `analyze_sentiment(articles: List[Dict]) -> Dict`: Analyzes sentiment of news articles.

### 9. Database Operations (`db.py`)
- **Purpose**: Handles database operations for storing analysis results.
- **Functions**:
  - `create_db(db_file: str) -> dict`: Creates or loads a JSON database.
  - `insert_analysis(db: dict, analysis: Dict)`: Inserts a new analysis into the JSON database.

### 10. Main Script (`kraken_futures_poc.py`)
- **Purpose**: Main entry point for the system, orchestrates data fetching, analysis, and formatting.
- **Functions**:
  - `fetch_tickers(client) -> str`: Fetches all tickers from the client.
  - `filter_coins(tickers_json: str) -> Tuple[List[str], List[str]]`: Filters top stable coins and altcoins.
  - `analyze_market(client, symbol: str) -> Tuple[Dict, str]`: Analyzes market for a specific symbol and returns analysis and summary.
  - `print_summaries(summaries: List[str])`: Prints all summaries together at the end.
  - `select_best_coin(analyses: Dict) -> str`: Selects the best coin based on detailed analysis.
  - `main()`: Main function to analyze all supported symbols and print results.

### 11. Coin Filtering (`analysis/coin_filter.py`)
- **Purpose**: Fetches and filters coins by volume to identify top altcoins and stable coins.
- **Functions**:
  - `filter_top_coins(tickers_json: str, alt_limit: int = 5, stable_limit: int = 5) -> Tuple[List[str], List[str]]`:
    Parses the JSON from Kraken’s `get_tickers`, then selects top `alt_limit` altcoins and top `stable_limit` stable coins by volume.

### 12. Buy Coin Module (`buy_coin.py`)
- **Purpose**: Buys the best coin based on the analysis.
- **Functions**:
  - `get_best_coin(analyses: Dict) -> str`: Selects the best coin based on detailed analysis.
  - `buy_coin(client, symbol: str, amount_usd: float) -> Dict`: Buys a specified amount of the best coin.
  - `main()`: Main function to load analysis results, select the best coin, and place the buy order.

## Data Flow
1. **Client Creation**: `kraken_client_factory.py` creates a client instance using API keys.
2. **Symbol Configuration**: `config/symbols.py` provides configuration for supported symbols.
3. **Market Data Fetching**: `analysis/market_data.py` fetches and processes market data.
4. **Technical Analysis**: `analysis/technical.py` calculates technical indicators.
5. **Trading Signals**: `analysis/signals.py` generates trading signals based on technical data.
6. **Advanced Trading Strategies**: `analysis/strategies.py` implements advanced trading strategies.
7. **News and Sentiment Analysis**: `analysis/news.py` fetches and analyzes news articles for sentiment.
8. **LLM Formatting**: `analysis/llm_formatter.py` formats the data for LLM consumption.
9. **Database Operations**: `db.py` handles database operations for storing analysis results.
10. **Main Script Execution**: `kraken_futures_poc.py` orchestrates the entire process and prints the results.
11. **Coin Filtering**: `analysis/coin_filter.py` helps select top coin lists to analyze.
12. **Buy Coin Execution**: `buy_coin.py` selects the best coin based on analysis and places a buy order.

## Example Usage
To run the analysis for all supported symbols:
```bash
python kraken_futures_poc.py
```

To buy the best coin based on the analysis:
```bash
python buy_coin.py
```

## Future Enhancements
- **Use Technical Analysis to Buy the Best Coin**: Enhance the system to use technical analysis data to make informed buy decisions.
- **Track Buys and Current Holdings**: Implement functionality to track all buys and current holdings, including the amount paid, current value, and profit/loss.
- **Decide to Sell or Hold**: Develop logic to decide whether to sell or hold a coin based on current market conditions and technical analysis.
- **Track Current Coins Held**: Maintain a record of all current coins held, including the amount, purchase price, and current value.
- **Track Profit/Loss**: Track the profit or loss for each coin held, including the initial investment and current value.
- **Track Exposure**: Monitor the total exposure in the market, including the total amount invested and the distribution across different coins.
- **Store Data in TinyDB**: Use TinyDB to store detailed information about current holdings, transactions, and market data.
- **Data Collection for Model Training**: Collect comprehensive data to train a model like ChatGPT, including market conditions, trading decisions, and outcomes.
- **Enhance Error Handling and Logging**: Improve error handling and logging to ensure robust and reliable operation.
- **Integrate with External Data Sources**: Integrate with external data sources for additional market insights and sentiment analysis.
- **Paper Trading & Order Simulation**: Implement a complete paper trading mode to simulate buys/sells, generating fake orders and storing transaction details without risking real funds.
- **Position Management & Trade History**: Maintain detailed records of open/closed positions, realized/unrealized PnL, time of entry/exit, and order fill prices.
- **Reason Codes & Strategy Metadata**: Log the rationale behind buying/selling decisions, referencing signal triggers (e.g., RSI oversold) or fundamental data.
- **Advanced Data Collection for LLM Training**: Expand the data captured during trades (e.g., user inputs, code outputs, model recommendations) to build a high-quality dataset for fine-tuning.
- **Backtesting & Replay Mode**: Allow the system to replay historical data for evaluating changes in technical indicators, trading signals, or LLM-based predictions over past market conditions.
