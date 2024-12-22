import cfRestApiV3 as cfApi

def create_futures_client(key_file='kraken.key'):
    """Factory function to create a properly configured Kraken Futures client"""
    with open(key_file, 'r') as f:
        api_key = f.readline().strip()
        secret_key = f.readline().strip()

    return cfApi.cfApiMethods(
        apiPath="https://demo-futures.kraken.com",  # Changed from api_path to apiPath
        timeout=20,
        apiPublicKey=api_key,  # These were already correct
        apiPrivateKey=secret_key,
        checkCertificate=True,
        useNonce=False
    )
