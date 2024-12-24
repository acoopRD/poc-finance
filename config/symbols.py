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
    },
    'PF_ARBUSD': {
        'min_size': 1,
        'price_decimals': 2,
        'futures_symbol': 'PF_ARBUSD',
        'perp_symbol': '',
    },
    'PF_SHIBUSD': {
        'min_size': 100000,
        'price_decimals': 8,
        'futures_symbol': 'PF_SHIBUSD',
        'perp_symbol': '',
    },
    'PI_ETHUSD': {
        'min_size': 0.01,
        'price_decimals': 2,
        'futures_symbol': '',
        'perp_symbol': 'PI_ETHUSD',
    },
    'PF_ALGOUSD': {
        'futures_symbol': 'PF_ALGOUSD',
        'perp_symbol': '',
        'min_size': 10,
        'price_decimals': 4
    },
    'PI_XBTUSD': {
        'futures_symbol': 'PI_XBTUSD',
        'perp_symbol': '',
        'min_size': 0.001,
        'price_decimals': 1
    },
    'PF_XLMUSD': {
        'futures_symbol': 'PF_XLMUSD',
        'perp_symbol': '',
        'min_size': 10,
        'price_decimals': 4
    },
    'PF_XRPUSD': {
        'futures_symbol': 'PF_XRPUSD',
        'perp_symbol': '',
        'min_size': 10,
        'price_decimals': 4
    }
    # Add more symbols as needed
}

def get_symbol_config(symbol: str) -> dict:
    """Get symbol configuration"""
    return SUPPORTED_SYMBOLS.get(symbol.upper(), None)
