from kraken.futures import KrakenFuturesWSClient
import asyncio
import json
import os

def read_credentials():
    try:
        with open('kraken.key', 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                return lines[0].strip(), lines[1].strip()
            else:
                raise ValueError("kraken.key must contain API key and secret")
    except FileNotFoundError:
        raise FileNotFoundError("kraken.key file not found")

class KrakenFuturesAPI:
    def __init__(self, api_key, api_secret, sandbox=True):
        self.client = KrakenFuturesWSClient(
            post_only=False,
            sandbox=sandbox,
            debug=True
        )
        self.api_key = api_key
        self.api_secret = api_secret
        print(f"Initialized with API key: {api_key[:10]}... (Sandbox: {sandbox})")

    async def subscribe_fills(self):
        await self.client.connect()
        self.client.add_auth_headers(self.api_key, self.api_secret)
        await self.client.subscribe_fills()

        try:
            while True:
                msg = await self.client.receive()
                print(f"Received: {json.dumps(msg, indent=2)}")
                if 'fills' in msg:
                    return msg
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.client.disconnect()

async def main():
    try:
        api_key, api_secret = read_credentials()
        client = KrakenFuturesAPI(api_key, api_secret, sandbox=True)
        fills = await client.subscribe_fills()
        
        if fills:
            print(f"Fills data: {json.dumps(fills, indent=2)}")
        else:
            print("No valid fills data received")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())