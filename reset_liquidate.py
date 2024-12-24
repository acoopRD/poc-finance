import logging
import json
import time
from kraken_client_factory import create_futures_client

logging.basicConfig(level=logging.INFO)

def get_instruments(client):
    """Get available trading instruments"""
    response = json.loads(client.get_instruments())
    instruments = response.get('instruments', [])
    tradeable = [i for i in instruments if i.get('tradeable', False)]
    logging.info(f"Found {len(tradeable)} tradeable instruments")
    for i in tradeable:
        logging.debug(f"Instrument: {i['symbol']} - Min size: {i.get('minTradeSize', 'unknown')}")
    return tradeable

def get_balance(client):
    """Get account balance"""
    response = json.loads(client.get_accounts())
    balances = response.get('accounts', {}).get('cash', {}).get('balances', {})
    logging.info(f"Raw balances: {balances}")
    return balances

def get_trading_pair(instruments, base_currency):
    """Find appropriate trading pair using Kraken's symbol conventions"""
    currency_map = {
        'xbt': 'XBT',
        'bch': 'BCH',
        'eth': 'ETH',
        'ltc': 'LTC',
        'xrp': 'XRP',
        'usdc': 'USDC',
        'usdt': 'USDT',
        'eur': 'EUR',
        'gbp': 'GBP'
    }
    
    base = currency_map.get(base_currency.lower(), base_currency.upper())
    
    # Try different symbol patterns
    patterns = [
        f"PI_{base}USD",   # Perpetual
        f"PF_{base}USD",   # Futures
        f"FI_{base}USD",   # Other futures
        f"CF_{base}USD"    # Cash-settled futures
    ]
    
    for pattern in patterns:
        pair = next((i for i in instruments if i['symbol'] == pattern), None)
        if pair:
            logging.info(f"Found trading pair {pair['symbol']} for {base_currency}")
            return pair
    
    logging.error(f"No trading pair found for {base_currency}")
    return None

def execute_market_order(client, instrument, side, size):
    """Execute a market order with proper parameters"""
    try:
        min_size = float(instrument.get('minTradeSize', 1))
        if float(size) < min_size:
            logging.error(f"Size {size} is below minimum {min_size} for {instrument['symbol']}")
            return None
            
        logging.info(f"Executing {side} order for {size} {instrument['symbol']} (min size: {min_size})")
        response = client.send_order(
            orderType='mkt',
            symbol=instrument['symbol'],
            side=side.lower(),
            size=float(size),
            limitPrice=0
        )
        
        result = json.loads(response)
        if result.get('result') == 'success':
            status = result.get('sendStatus', {}).get('status')
            if status == 'invalidSize':
                logging.error(f"Invalid size for {instrument['symbol']}: {size}")
                return None
            logging.info(f"Order executed successfully: {response}")
            return result
        else:
            logging.error(f"Order failed: {response}")
            return None
            
    except Exception as e:
        logging.error(f"Order error for {instrument['symbol']}: {str(e)}")
        return None

def convert_to_usd(client, balance, instruments):
    """Convert all assets to USD"""
    successful_conversions = []
    for asset, amount in balance.items():
        if asset.lower() not in ['usd', 'usdt'] and float(amount) > 0:
            pair = get_trading_pair(instruments, asset)
            if pair:
                min_size = float(pair.get('minTradeSize', 1))
                if float(amount) >= min_size:
                    result = execute_market_order(client, pair, 'sell', amount)
                    if result:
                        successful_conversions.append(asset)
                        time.sleep(2)  # Wait between orders
                else:
                    logging.error(f"Amount {amount} of {asset} is below the minimum trade size {min_size}")
            else:
                logging.error(f"No trading pair found for {asset}")

def main():
    client = create_futures_client()
    instruments = get_instruments(client)
    
    # Get initial balance
    balance = get_balance(client)
    logging.info(f"Initial balance: {balance}")
    
    # Convert everything to USD first
    convert_to_usd(client, balance, instruments)
    
    # Wait for orders to settle
    time.sleep(5)
    
    # Get final balance
    final_balance = get_balance(client)
    logging.info(f"Final balance: {final_balance}")

if __name__ == "__main__":
    main()
