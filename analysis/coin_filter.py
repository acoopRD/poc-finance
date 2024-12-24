import json

STABLE_COIN_SYMBOLS = {"USDT", "USDC", "DAI", "BUSD", "UST"}  # Extend as needed
QUOTE_CURRENCIES = {"USD", "EUR", "JPY"}  # Extend as needed

def filter_top_coins(tickers_json: str, alt_limit: int = 5, stable_limit: int = 5):
    """
    Filter the top 'alt_limit' altcoins and top 'stable_limit' stable coins by volume.
    'tickers_json' is a JSON string from Kraken's get_tickers call.
    """
    all_tickers = json.loads(tickers_json).get('tickers', [])
    # Filter stable coins vs. altcoins
    stable = []
    altcoins = []
    for t in all_tickers:
        symbol = t.get('symbol', '')
        vol = float(t.get('vol24h', 0))
        if any(s in symbol for s in STABLE_COIN_SYMBOLS) and any(q in symbol for q in QUOTE_CURRENCIES):
            stable.append((symbol, vol))
        elif any(q in symbol for q in QUOTE_CURRENCIES):
            altcoins.append((symbol, vol))
    # Sort by volume descending
    stable.sort(key=lambda x: x[1], reverse=True)
    altcoins.sort(key=lambda x: x[1], reverse=True)
    # Return top slices
    return [s[0] for s in stable[:stable_limit]], [a[0] for a in altcoins[:alt_limit]]