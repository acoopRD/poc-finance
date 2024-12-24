import logging
from kraken_client_factory import create_futures_client
from analysis.market_data import get_market_data
from config.symbols import get_symbol_config
from tinydb import TinyDB, Query
import json
import time

logging.basicConfig(level=logging.INFO)

db = TinyDB('trading_data.json')

def get_best_coin(analyses):
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

def buy_coin(client, symbol, amount_usd):
    """Buy a specified amount of the best coin"""
    symbol_config = get_symbol_config(symbol)
    if not symbol_config:
        logging.error(f"Unsupported symbol: {symbol}")
        return
    
    try:
        # Get market data for symbol
        market_data = get_market_data(client, symbol_config['futures_symbol'] or symbol_config['perp_symbol'])
        current_price = market_data["price_action"]["current_price"]
        
        # Calculate the amount to buy
        amount_to_buy = amount_usd / current_price
        
        # Simulate a market buy order (paper trading)
        order = {
            'symbol': symbol,
            'amount_usd': amount_usd,
            'amount_to_buy': amount_to_buy,
            'price': current_price,
            'timestamp': time.time(),
            'type': 'buy'
        }
        db.insert(order)
        
        logging.info(f"Simulated buy order: {order}")
        
        return order
        
    except Exception as e:
        logging.error(f"Error buying {symbol}: {str(e)}")
        return None

def main():
    client = create_futures_client()
    
    # Load analysis results
    with open("analysis_results.json", 'r') as file:
        analyses = json.load(file)
    
    # Select the best coin for a buy
    best_coin = get_best_coin(analyses)
    if best_coin:
        logging.info(f"Best coin to buy: {best_coin}")
        buy_coin(client, best_coin, 100)
    else:
        logging.error("No suitable coin found for buying")

if __name__ == "__main__":
    main()
