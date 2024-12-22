import krakenex
import time
import json
import requests
import hmac
import hashlib
import base64
import sys
import urllib.parse

class TradingBot:
    def __init__(self, debug=True):
        self.kraken = krakenex.API()
        self.kraken.load_key('kraken.key')
        self.base_url = 'https://demo-futures.kraken.com/derivatives'
        self.pair = 'PI_XBTUSD'
        self.debug = debug
        
        # Load keys from properly formatted file
        self.api_key = self.kraken.key
        self.api_secret = self.kraken.secret
        
        if debug:
            print(f"API Key length: {len(self.api_key)}")
            print(f"API Secret length: {len(self.api_secret)}")
        print(f"Initialized Kraken Futures API with sandbox for {self.pair}")

    def get_price(self):
        try:
            response = requests.get(f"{self.base_url}/api/v3/tickers")
            data = response.json()
            
            if response.status_code != 200:
                print(f"Error: {data.get('error', 'Unknown error')}")
                return None
                
            for ticker in data.get('tickers', []):
                if ticker['symbol'] == self.pair:
                    if self.debug:
                        print(f"Debug - Ticker data: {json.dumps(ticker, indent=2)}")
                    return float(ticker['last'])
            return None
        except Exception as e:
            print(f"Error getting price: {e}")
            return None

    def get_position(self):
        try:
            nonce = str(int(time.time() * 1000))
            endpoint = "/api/v3/openpositions"
            
            # Fix authentication per Kraken Futures docs
            postdata = {
                "nonce": nonce,
                "orderType": "lmt",
                "symbol": self.pair
            }
            
            # Create signature
            post_data = urllib.parse.urlencode(postdata)
            message = endpoint + nonce + post_data
            signature = hmac.new(
                base64.b64decode(self.api_secret),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()

            # Updated headers format
            headers = {
                "APIKey": self.api_key,
                "Nonce": nonce,
                "Authent": signature,
                "Content-Type": "application/x-www-form-urlencoded"
            }

            response = requests.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                data=postdata
            )
            
            data = response.json()
            if self.debug:
                print(f"Position data: {json.dumps(data, indent=2)}")
            return data
            
        except Exception as e:
            print(f"Error getting position: {str(e)}")
            return None

    def run(self):
        print("Starting trading bot...")
        try:
            while True:
                price = self.get_price()
                position = self.get_position()
                if price:
                    print(f"Current {self.pair} price: {price}")
                    print(f"Current position: {position}")
                time.sleep(60)
        except KeyboardInterrupt:
            print("\nShutting down bot...")
            sys.exit(0)

def main():
    bot = TradingBot(debug=True)
    bot.run()

if __name__ == "__main__":
    main()