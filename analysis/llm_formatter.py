from typing import Dict
from datetime import datetime

def format_llm_analysis(market_data: Dict, symbol_config: Dict) -> Dict:
    """Format comprehensive market analysis for LLM consumption"""
    ticker = market_data.get('ticker', {})
    technical_data = market_data.get('technical', {})
    orderbook = market_data.get('orderbook', {})
    orderbook_analysis = market_data.get('orderbook_analysis', {})
    liquidity = market_data.get('liquidity', {})
    news_sentiment = market_data.get('news_sentiment', {})
    
    return {
        "analysis_version": "1.0",
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol_config.get('futures_symbol') or symbol_config.get('perp_symbol'),
        "market_context": {
            "price_action": {
                "current_price": ticker.get('markPrice'),
                "24h_high": ticker.get('high24h'),
                "24h_low": ticker.get('low24h'),
                "24h_volume": ticker.get('vol24h'),
                "price_change_24h": (ticker.get('markPrice', 0) - ticker.get('last', 0))
            },
            "market_depth": {
                "top_bids": orderbook.get('orderBook', {}).get('bids', [])[:3],
                "top_asks": orderbook.get('orderBook', {}).get('asks', [])[:3],
                "order_imbalance": orderbook_analysis.get('pressure_ratio', 0)
            }
        },
        "technical_analysis": {
            "momentum_indicators": {
                "rsi": technical_data.get("rsi"),
                "macd_histogram": technical_data.get("macd", {}).get("histogram"),
                "trend_direction": technical_data.get("trend", {}).get("direction"),
                "trend_strength": technical_data.get("trend", {}).get("strength")
            },
            "volatility_metrics": {
                "volatility_index": technical_data.get("volatility", {}).get("volatility_index"),
                "price_range": technical_data.get("volatility", {}).get("price_range")
            },
            "abcd_pattern_detection": technical_data.get("abcde_pattern", False)
        },
        "market_dynamics": {
            "liquidity": {
                "bid_depth_total": liquidity.get("bid_depth", 0),
                "ask_depth_total": liquidity.get("ask_depth", 0),
                "spread_percentage": liquidity.get("spread_percentage", 0)
            },
            "market_sentiment": {
                "funding_rate": ticker.get("fundingRate", 0),
                "open_interest": ticker.get("openInterest", 0),
                "buy_pressure": orderbook_analysis.get("pressure_ratio", 0),
                "news_sentiment": news_sentiment.get("sentiment_score", 0)
            }
        },
        "trading_signals": {
            "primary_indicators": {
                "rsi_signal": "oversold" if technical_data.get("rsi", 50) < 30 else 
                             "overbought" if technical_data.get("rsi", 50) > 70 else "neutral",
                "macd_signal": "bullish" if technical_data.get("macd", {}).get("histogram", 0) > 0 else 
                              "bearish" if technical_data.get("macd", {}).get("histogram", 0) < 0 else "neutral",
                "trend_signal": technical_data.get("trend", {}).get("direction", "neutral")
            },
            "market_conditions": {
                "liquidity_state": "high" if liquidity.get("spread_percentage", 1) < 0.0005 else 
                                  "low" if liquidity.get("spread_percentage", 1) > 0.002 else "normal",
                "volatility_state": "high" if technical_data.get("volatility", {}).get("volatility_index", 0) > 0.002 else 
                                  "low" if technical_data.get("volatility", {}).get("volatility_index", 0) < 0.0005 else "normal"
            }
        },
        "symbol_specific": {
            "min_trade_size": symbol_config['min_size'],
            "price_decimals": symbol_config['price_decimals'],
            "has_futures": bool(symbol_config['futures_symbol']),
            "has_perpetual": bool(symbol_config['perp_symbol'])
        }
    }
