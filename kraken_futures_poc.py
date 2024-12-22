import json
from kraken_client_factory import create_futures_client

def get_account_overview(client):
    """Get overview of account positions and orders"""
    positions = client.get_openpositions()
    orders = client.get_openorders()
    accounts = client.get_accounts()
    tickers = client.get_tickers()
    
    return {
        "positions": positions,
        "orders": orders,
        "accounts": accounts,
        "tickers": tickers
    }

def main():
    client = create_futures_client()  # Simple, clean, and clear
    overview = get_account_overview(client)
    print(json.dumps(overview, indent=2))

if __name__ == "__main__":
    main()
