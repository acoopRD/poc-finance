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

### 9. Main Script (`kraken_futures_poc.py`)
- **Purpose**: Main entry point for the system, orchestrates data fetching, analysis, and formatting.
- **Functions**:
  - `analyze_market(client, symbol: str) -> Dict`: Analyzes market for a specific symbol.
  - `main()`: Main function to analyze all supported symbols and print results.

## Data Flow
1. **Client Creation**: `kraken_client_factory.py` creates a client instance using API keys.
2. **Symbol Configuration**: `config/symbols.py` provides configuration for supported symbols.
3. **Market Data Fetching**: `analysis/market_data.py` fetches and processes market data.
4. **Technical Analysis**: `analysis/technical.py` calculates technical indicators.
5. **Trading Signals**: `analysis/signals.py` generates trading signals based on technical data.
6. **Advanced Trading Strategies**: `analysis/strategies.py` implements advanced trading strategies.
7. **News and Sentiment Analysis**: `analysis/news.py` fetches and analyzes news articles for sentiment.
8. **LLM Formatting**: `analysis/llm_formatter.py` formats the data for LLM consumption.
9. **Main Script Execution**: `kraken_futures_poc.py` orchestrates the entire process and prints the results.

## Example Usage
To run the analysis for all supported symbols:
```bash
python kraken_futures_poc.py
```

## Future Enhancements
- Add support for more symbols.
- Integrate additional technical indicators.
- Implement advanced trading strategies.
- Enhance error handling and logging.
- Integrate with external data sources for news and sentiment analysis.
