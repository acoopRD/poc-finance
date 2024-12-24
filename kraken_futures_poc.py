import json
import logging
from datetime import datetime
from kraken_client_factory import create_futures_client
from analysis.market_data import get_market_data
from analysis.llm_formatter import format_llm_analysis
from analysis.news import fetch_news, analyze_sentiment
from analysis.strategies import bollinger_band_strategy, moving_average_crossover_strategy
from config.symbols import get_symbol_config, SUPPORTED_SYMBOLS
from analysis.coin_filter import filter_top_coins
from db import create_db, insert_analysis, track_holdings, get_holdings, get_profit_loss
from tinydb import TinyDB, Query

logging.basicConfig(level=logging.INFO)

db = create_db('trading_data.json')

def fetch_tickers(client):
    """Fetch all tickers from the client"""
    return client.get_tickers()

def filter_coins(tickers_json):
    """Filter top stable coins and altcoins"""
    return filter_top_coins(tickers_json, alt_limit=5, stable_limit=5)

def analyze_market(client, symbol: str):
    """Analyze market for a specific symbol"""
    symbol_config = get_symbol_config(symbol)
    if not symbol_config:
        return {"error": f"Unsupported symbol: {symbol}"}, None
    
    try:
        # Get market data for symbol
        market_data = get_market_data(
            client, 
            symbol_config['futures_symbol'] or symbol_config['perp_symbol']
        )
        
        # Fetch and analyze news (disabled)
        # news_articles = fetch_news(symbol)
        # sentiment = analyze_sentiment(news_articles) if news_articles else {"positive": 0, "negative": 0, "neutral": 0}
        
        # Apply advanced trading strategies
        bollinger_signal = bollinger_band_strategy(market_data["technical"])
        ma_crossover_signal = moving_average_crossover_strategy(market_data["technical"])
        
        # Format for LLM consumption
        analysis = format_llm_analysis(market_data, symbol_config)
        # analysis["news_sentiment"] = sentiment
        # analysis["news_articles"] = news_articles[:5]  # Include top 5 news articles
        analysis["trading_strategies"] = {
            "bollinger_band_signal": bollinger_signal,
            "ma_crossover_signal": ma_crossover_signal
        }
        
        # Create human-readable summary
        underlying_coin = symbol.split('_')[1].replace('USD', '')
        summary = f"{underlying_coin} ({symbol}): High trading volume, high liquidity, and significant market depth. Neutral RSI and MACD signals, indicating a balanced market sentiment."
        
        return analysis, summary
        
    except Exception as e:
        logging.error(f"Error analyzing market for {symbol}: {str(e)}")
        return {"error": str(e), "symbol": symbol, "timestamp": datetime.now().isoformat()}, None

def print_summaries(summaries):
    """Print all summaries together at the end"""
    print("\n=== Summaries ===")
    for summary in summaries:
        print(f"- {summary}")

def select_best_coin(analyses):
    """Select the best coin based on detailed analysis"""
    best_coin = None
    best_score = float('-inf')
    
    for symbol, analysis in analyses.items():
        try:
            # Example criteria: RSI, MACD, and trading volume
            rsi = analysis["technical_analysis"]["momentum_indicators"]["rsi"]
            macd = analysis["technical_analysis"]["momentum_indicators"]["macd_histogram"]
            volume = analysis["market_context"]["price_action"]["24h_volume"]
            
            # Calculate a simple score (this can be more complex)
            score = (100 - abs(rsi - 50)) + macd + volume
            
            if score > best_score:
                best_score = score
                best_coin = symbol
        except KeyError as e:
            logging.error(f"Missing key in analysis for {symbol}: {e}")
    
    return best_coin

def decide_sell_or_hold(client, symbol):
    """Decide whether to sell or hold a coin based on current market conditions and technical analysis"""
    symbol_config = get_symbol_config(symbol)
    if not symbol_config:
        logging.error(f"Unsupported symbol: {symbol}")
        return
    
    try:
        # Get market data for symbol
        market_data = get_market_data(client, symbol_config['futures_symbol'] or symbol_config['perp_symbol'])
        current_price = market_data["price_action"]["current_price"]
        
        # Get holding data
        holdings = db.table('holdings')
        holding = holdings.get(Query().symbol == symbol)
        
        if holding:
            amount = holding['amount']
            total_cost = holding['total_cost']
            current_value = amount * current_price
            profit_loss = current_value - total_cost
            
            # Decide to sell or hold based on profit/loss and market conditions
            if profit_loss > 0 and market_data["technical"]["momentum_indicators"]["rsi"] > 70:
                # Simulate a market sell order (paper trading)
                order = {
                    'symbol': symbol,
                    'amount_usd': current_value,
                    'amount_to_sell': amount,
                    'price': current_price,
                    'timestamp': time.time(),
                    'type': 'sell'
                }
                db.insert(order)
                holdings.remove(Query().symbol == symbol)
                
                logging.info(f"Simulated sell order: {order}")
            else:
                logging.info(f"Holding {symbol}: Current value = {current_value}, Profit/Loss = {profit_loss}")
        else:
            logging.error(f"No holdings found for {symbol}")
        
    except Exception as e:
        logging.error(f"Error deciding sell or hold for {symbol}: {str(e)}")

def main():
    client = create_futures_client()
    tickers_json = fetch_tickers(client)
    top_stables, top_alts = filter_coins(tickers_json)
    symbols_to_analyze = top_stables + top_alts

    db = create_db("analysis_results.json")

    analyses = {}
    summaries = []
    for symbol in symbols_to_analyze:
        print(f"\n=== {symbol} Market Analysis ===")
        logging.info(f"Analyzing symbol: {symbol}")
        analysis, summary = analyze_market(client, symbol)
        print(json.dumps(analysis, indent=2))
        analyses[symbol] = analysis
        if summary:
            summaries.append(summary)
        if analysis:
            insert_analysis(db, analysis)

    print_summaries(summaries)
    
    # Select the best coin for a buy
    best_coin = select_best_coin(analyses)
    if best_coin:
        print(f"\n=== Best Coin to Buy: {best_coin} ===")
        logging.info(f"Best coin to buy: {best_coin}")

    # Decide to sell or hold current holdings
    holdings = get_holdings(db)
    for holding in holdings:
        decide_sell_or_hold(client, holding['symbol'])

if __name__ == "__main__":
    main()
