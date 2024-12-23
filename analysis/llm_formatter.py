from typing import Dict
from datetime import datetime

def format_llm_analysis(market_data: Dict, technical_data: Dict, orderbook_data: Dict) -> Dict:
    """Format comprehensive market analysis for LLM consumption"""
    return {
        "market_context": {
            "price_action": {
                "current_price": market_data.get('markPrice'),
                "24h_high": market_data.get('high24h'),
                "24h_low": market_data.get('low24h'),
                "24h_volume": market_data.get('vol24h'),
                "price_change_24h": (market_data.get('markPrice', 0) - market_data.get('last', 0))
            },
            "market_depth": {
                "top_bids": orderbook_data.get('orderBook', {}).get('bids', [])[:3],
                "top_asks": orderbook_data.get('orderBook', {}).get('asks', [])[:3],
                "order_imbalance": orderbook_data.get('pressure_ratio', 0)
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
            }
        },
        "market_dynamics": {
            "liquidity": {
                "bid_depth_total": orderbook_data.get("bid_depth", 0),
                "ask_depth_total": orderbook_data.get("ask_depth", 0),
                "spread_percentage": orderbook_data.get("spread_percentage", 0)
            },
            "market_sentiment": {
                "funding_rate": market_data.get("fundingRate", 0),
                "open_interest": market_data.get("openInterest", 0),
                "buy_pressure": orderbook_data.get("pressure_ratio", 0)
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
                "liquidity_state": "high" if orderbook_data.get("spread_percentage", 1) < 0.0005 else 
                                  "low" if orderbook_data.get("spread_percentage", 1) > 0.002 else "normal",
                "volatility_state": "high" if technical_data.get("volatility", {}).get("volatility_index", 0) > 0.002 else 
                                  "low" if technical_data.get("volatility", {}).get("volatility_index", 0) < 0.0005 else "normal"
            }
        },
        "timestamp": datetime.now().isoformat()
    }
