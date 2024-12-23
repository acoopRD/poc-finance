import json
from datetime import datetime, timedelta
from kraken_client_factory import create_futures_client
from analysis.technical import calculate_rsi, calculate_macd, calculate_volatility, detect_trend
from analysis.market_data import analyze_orderbook, analyze_liquidity, process_historical_prices
from analysis.llm_formatter import format_llm_analysis

def get_market_analysis(client):
    """Get comprehensive market analysis data"""
    try:
        # Fetch market data
        orderbook = json.loads(client.get_orderbook('PI_XBTUSD'))
        all_tickers = json.loads(client.get_tickers())
        btc_ticker = next((t for t in all_tickers.get('tickers', []) 
                       if t.get('symbol') in ['PI_XBTUSD', 'PF_XBTUSD']), {})
        
        # Get historical data
        since = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
        historical_prices = client.get_market_price('PI_XBTUSD', since=since)
        price_data = process_historical_prices(historical_prices)
        
        # Calculate technical indicators
        technical_data = {
            "rsi": calculate_rsi(price_data),
            "macd": calculate_macd(price_data),
            "volatility": calculate_volatility(price_data),
            "trend": detect_trend(price_data)
        }
        
        # Analyze market structure
        orderbook_analysis = {
            **analyze_orderbook(orderbook),
            **analyze_liquidity(orderbook)
        }
        
        # Format for LLM consumption
        return format_llm_analysis(btc_ticker, technical_data, orderbook_analysis)
        
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now().isoformat()}

def main():
    client = create_futures_client()
    analysis = get_market_analysis(client)
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()
