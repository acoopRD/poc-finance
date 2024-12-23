from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
from analysis.technical import calculate_rsi, calculate_macd, calculate_volatility, detect_trend

def get_historical_data(client, symbol: str) -> List[float]:
    """Get and process historical price data"""
    try:
        since = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)
        historical_prices = client.get_market_price(symbol, since=since)
        return process_historical_prices(historical_prices)
    except Exception as e:
        print(f"Error getting historical data for {symbol}: {str(e)}")
        return []

def analyze_orderbook(orderbook: Dict) -> Dict:
    """Analyze order book for market sentiment"""
    if not orderbook or not isinstance(orderbook, dict):
        return {"pressure_ratio": 0, "spread": 0}
        
    book = orderbook.get('orderBook', {})
    bids = book.get('bids', [])
    asks = book.get('asks', [])
    
    try:
        bid_volume = sum(float(bid[1]) for bid in bids[:10] if len(bid) > 1)
        ask_volume = sum(float(ask[1]) for ask in asks[:10] if len(ask) > 1)
        spread = float(asks[0][0]) - float(bids[0][0]) if bids and asks else 0
        
        return {
            "pressure_ratio": bid_volume / ask_volume if ask_volume else 0,
            "spread": spread
        }
    except (IndexError, ValueError, ZeroDivisionError):
        return {"pressure_ratio": 0, "spread": 0}

def analyze_liquidity(orderbook: Dict) -> Dict:
    """Analyze market liquidity"""
    if not orderbook or not isinstance(orderbook, dict):
        return {"bid_depth": 0, "ask_depth": 0, "spread_percentage": 0}
        
    book = orderbook.get('orderBook', {})
    bids = book.get('bids', [])
    asks = book.get('asks', [])
    
    try:
        bid_depth = sum(float(bid[1]) for bid in bids if len(bid) > 1)
        ask_depth = sum(float(ask[1]) for ask in asks if len(ask) > 1)
        spread_percentage = (float(asks[0][0]) - float(bids[0][0])) / float(bids[0][0]) if bids and asks else 0
        
        return {
            "bid_depth": bid_depth,
            "ask_depth": ask_depth,
            "spread_percentage": spread_percentage
        }
    except (IndexError, ValueError, ZeroDivisionError):
        return {"bid_depth": 0, "ask_depth": 0, "spread_percentage": 0}

def analyze_funding_rate(ticker: Dict) -> str:
    """Analyze funding rate for signal"""
    # ...existing funding rate analysis code...

def process_historical_prices(historical_data: List) -> List[float]:
    """Process historical price data into clean price list"""
    if not historical_data or not isinstance(historical_data, list):
        return []
        
    prices = []
    try:
        for p in historical_data:
            if isinstance(p, dict) and 'event' in p:
                event = p.get('event', {})
                if isinstance(event, dict) and 'MarkPriceChanged' in event:
                    price_str = event['MarkPriceChanged'].get('price')
                    if price_str:
                        try:
                            price = float(price_str)
                            prices.append(price)
                        except (ValueError, TypeError):
                            continue
        return prices
    except Exception:
        return []

def get_market_data(client, symbol: str) -> Dict:
    """Get comprehensive market data for a symbol"""
    try:
        # Get market data
        orderbook = json.loads(client.get_orderbook(symbol))
        all_tickers = json.loads(client.get_tickers())
        ticker = next((t for t in all_tickers.get('tickers', []) 
                    if t.get('symbol') == symbol), {})
        
        # Get historical data
        price_data = get_historical_data(client, symbol)
        
        # Calculate technical indicators
        technical_data = {
            "rsi": calculate_rsi(price_data),
            "macd": calculate_macd(price_data),
            "volatility": calculate_volatility(price_data),
            "trend": detect_trend(price_data)
        }
        
        orderbook_analysis = analyze_orderbook(orderbook)
        liquidity_analysis = analyze_liquidity(orderbook)
        
        return {
            "ticker": ticker,
            "orderbook": orderbook,
            "technical": technical_data,
            "orderbook_analysis": orderbook_analysis,
            "liquidity": liquidity_analysis
        }
    except Exception as e:
        print(f"Error getting market data for {symbol}: {str(e)}")
        return {}
