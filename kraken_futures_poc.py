import json
import logging
from datetime import datetime
from kraken_client_factory import create_futures_client
from analysis.market_data import get_market_data
from analysis.llm_formatter import format_llm_analysis
from analysis.news import fetch_news, analyze_sentiment
from analysis.strategies import bollinger_band_strategy, moving_average_crossover_strategy
from config.symbols import get_symbol_config, SUPPORTED_SYMBOLS

logging.basicConfig(level=logging.INFO)

def analyze_market(client, symbol: str):
    """Analyze market for a specific symbol"""
    symbol_config = get_symbol_config(symbol)
    if not symbol_config:
        return {"error": f"Unsupported symbol: {symbol}"}
    
    try:
        # Get market data for symbol
        market_data = get_market_data(
            client, 
            symbol_config['futures_symbol'] or symbol_config['perp_symbol']
        )
        
        # Fetch and analyze news
        news_articles = fetch_news(symbol)
        sentiment = analyze_sentiment(news_articles) if news_articles else {"positive": 0, "negative": 0, "neutral": 0}
        
        # Apply advanced trading strategies
        bollinger_signal = bollinger_band_strategy(market_data["technical"])
        ma_crossover_signal = moving_average_crossover_strategy(market_data["technical"])
        
        # Format for LLM consumption
        analysis = format_llm_analysis(market_data, symbol_config)
        analysis["news_sentiment"] = sentiment
        analysis["news_articles"] = news_articles[:5]  # Include top 5 news articles
        analysis["trading_strategies"] = {
            "bollinger_band_signal": bollinger_signal,
            "ma_crossover_signal": ma_crossover_signal
        }
        
        return analysis
        
    except Exception as e:
        logging.error(f"Error analyzing market for {symbol}: {str(e)}")
        return {"error": str(e), "symbol": symbol, "timestamp": datetime.now().isoformat()}

def main():
    client = create_futures_client()
    
    # Analyze all supported symbols
    analyses = {}
    for symbol in SUPPORTED_SYMBOLS.keys():
        print(f"\n=== {symbol} Market Analysis ===")  # Restored header
        logging.info(f"Analyzing symbol: {symbol}")
        analysis = analyze_market(client, symbol)
        print(json.dumps(analysis, indent=2))
        analyses[symbol] = analysis
    
    # Example of analyzing a single symbol
    # analysis = analyze_market(client, "BTC")
    # print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
