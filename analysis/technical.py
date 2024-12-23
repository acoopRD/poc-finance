from typing import List, Dict
import statistics

def calculate_rsi(prices: List[float], periods: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if not prices or len(prices) < periods:
        return None
    
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [change for change in changes if change > 0]
    losses = [-change for change in changes if change < 0]
    
    avg_gain = sum(gains[-periods:]) / periods if gains else 0
    avg_loss = sum(losses[-periods:]) / periods if losses else 0
    
    if avg_loss == 0:
        return 100 if avg_gain > 0 else 50
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices: List[float]) -> Dict:
    """Calculate MACD (12,26,9)"""
    if not prices or len(prices) < 26:
        return {
            "macd": 0,
            "signal": 0,
            "histogram": 0
        }
    
    # Calculate EMAs
    ema12 = sum(prices[-12:]) / 12
    ema26 = sum(prices[-26:]) / 26
    macd_line = ema12 - ema26
    signal_line = sum([macd_line] * 9) / 9
    
    return {
        "macd": macd_line,
        "signal": signal_line,
        "histogram": macd_line - signal_line
    }

def calculate_volatility(prices: List[float]) -> Dict:
    """Calculate volatility metrics"""
    if not prices or len(prices) < 2:
        return {
            "std_dev": 0,
            "price_range": 0,
            "volatility_index": 0
        }
    
    try:
        return {
            "std_dev": statistics.stdev(prices),
            "price_range": max(prices) - min(prices),
            "volatility_index": statistics.stdev(prices) / statistics.mean(prices)
        }
    except (ValueError, StatisticsError):
        return {
            "std_dev": 0,
            "price_range": 0,
            "volatility_index": 0
        }

def detect_trend(prices: List[float]) -> Dict:
    """Detect price trend and strength"""
    if not prices or len(prices) < 2:
        return {
            "direction": "neutral",
            "strength": 0
        }
    
    try:
        current_price = prices[-1]
        start_price = prices[0]
        direction = "bullish" if current_price > start_price else "bearish" if current_price < start_price else "neutral"
        strength = abs(current_price - start_price) / start_price if start_price != 0 else 0
        
        return {
            "direction": direction,
            "strength": strength
        }
    except (IndexError, ZeroDivisionError):
        return {
            "direction": "neutral",
            "strength": 0
        }

def calculate_bollinger_bands(prices: List[float], periods: int = 20, num_std_dev: int = 2) -> Dict:
    """Calculate Bollinger Bands"""
    if len(prices) < periods:
        return {"upper_band": 0, "lower_band": 0, "middle_band": 0}
    
    sma = sum(prices[-periods:]) / periods
    std_dev = statistics.stdev(prices[-periods:])
    upper_band = sma + (num_std_dev * std_dev)
    lower_band = sma - (num_std_dev * std_dev)
    
    return {"upper_band": upper_band, "lower_band": lower_band, "middle_band": sma}

def calculate_moving_average(prices: List[float], periods: int = 50) -> float:
    """Calculate Simple Moving Average"""
    if len(prices) < periods:
        return 0
    return sum(prices[-periods:]) / periods

def detect_abcde_pattern(prices: List[float]) -> bool:
    """
    Detect a hypothetical ABCDE pattern in the price list.
    Returns True if detected, False otherwise.
    """
    # This is a placeholder logic; replace with real pattern detection
    if len(prices) < 5:
        return False
    # Minimal example: checks if last 5 prices are in ascending order
    last_five = prices[-5:]
    return sorted(last_five) == last_five
