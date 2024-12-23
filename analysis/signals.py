from typing import Dict, List, Tuple
from datetime import datetime

def analyze_technical_signals(technical_data: Dict) -> List[Tuple[str, str, int]]:
    """Analyze technical indicators for trading signals"""
    signals = []
    
    # RSI Analysis
    if technical_data["rsi"]:
        rsi = technical_data["rsi"]
        if rsi < 30:
            signals.append(("BUY", f"RSI oversold ({rsi:.2f})", 3))
        elif rsi < 45:
            signals.append(("BUY", f"RSI approaching oversold ({rsi:.2f})", 1))
        elif rsi > 70:
            signals.append(("SELL", f"RSI overbought ({rsi:.2f})", 3))
        elif rsi > 65:
            signals.append(("SELL", f"RSI approaching overbought ({rsi:.2f})", 1))
    
    # MACD Analysis
    if technical_data["macd"]:
        macd = technical_data["macd"]["histogram"]
        if abs(macd) > 0.01:  # Only consider significant MACD movements
            if macd > 0:
                signals.append(("BUY", f"MACD positive momentum ({macd:.2f})", 2))
            else:
                signals.append(("SELL", f"MACD negative momentum ({macd:.2f})", 2))
    
    # Trend Analysis
    if technical_data["trend"]:
        strength = technical_data["trend"]["strength"]
        direction = technical_data["trend"]["direction"]
        if strength > 0.02:
            if direction == "bullish":
                signals.append(("BUY", f"Strong uptrend ({strength:.2%})", 3))
            else:
                signals.append(("SELL", f"Strong downtrend ({strength:.2%})", 3))
    
    return signals

def get_trading_recommendation(technical_data: Dict, ticker: Dict) -> Dict:
    """Generate trading recommendation based on technical indicators"""
    signals = analyze_technical_signals(technical_data)
    
    # Calculate weighted recommendation
    buy_weight = sum(weight for signal, _, weight in signals if signal == "BUY")
    sell_weight = sum(weight for signal, _, weight in signals if signal == "SELL")
    
    if buy_weight > sell_weight:
        action = "BUY"
        confidence = buy_weight / (buy_weight + sell_weight)
    elif sell_weight > buy_weight:
        action = "SELL"
        confidence = sell_weight / (buy_weight + sell_weight)
    else:
        action = "HOLD"
        confidence = 0.5

    return {
        "action": action,
        "confidence": confidence,
        "signals": [{"signal": signal, "reason": reason} for signal, reason, _ in signals],
        "timestamp": datetime.now().isoformat()
    }
