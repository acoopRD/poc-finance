from typing import Dict, List
from .technical import calculate_bollinger_bands, calculate_moving_average

def bollinger_band_strategy(technical_data: Dict) -> str:
    """Generate trading signal based on Bollinger Bands"""
    bollinger_bands = calculate_bollinger_bands(technical_data.get("prices", []))
    current_price = technical_data.get("prices", [])[-1] if technical_data.get("prices") else 0
    
    if current_price > bollinger_bands["upper_band"]:
        return "sell"
    elif current_price < bollinger_bands["lower_band"]:
        return "buy"
    else:
        return "hold"

def moving_average_crossover_strategy(technical_data: Dict) -> str:
    """Generate trading signal based on Moving Average Crossover"""
    short_ma = calculate_moving_average(technical_data.get("prices", []), periods=50)
    long_ma = calculate_moving_average(technical_data.get("prices", []), periods=200)
    
    if short_ma > long_ma:
        return "buy"
    elif short_ma < long_ma:
        return "sell"
    else:
        return "hold"
