SUPPORTED_SYMBOLS = {
    'BTC': {
        'futures_symbol': 'PI_XBTUSD',
        'perp_symbol': 'PF_XBTUSD',
        'min_size': 0.0001,
        'price_decimals': 1
    },
    'ETH': {
        'futures_symbol': 'PI_ETHUSD',
        'perp_symbol': 'PF_ETHUSD',
        'min_size': 0.001,
        'price_decimals': 2
    },
    'SOL': {
        'futures_symbol': None,  # No traditional futures
        'perp_symbol': 'PF_SOLUSD',
        'min_size': 0.1,
        'price_decimals': 3
    }
    # Add more symbols as needed
}

def get_symbol_config(symbol: str) -> dict:
    """Get symbol configuration"""
    return SUPPORTED_SYMBOLS.get(symbol.upper(), None)
