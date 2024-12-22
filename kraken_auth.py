import time
import hashlib
import hmac
import base64
import requests

# Your Kraken Demo API credentials
API_KEY = "EqJqV+hd5Md9YGGLCzq1g4llGQyR+8MvO7r/aMqan6Tu6Ngg2t0G1QNI"
API_SECRET = "H10pLVz6j1YfN/tFHjXXTyM+pxrUjLJqrxm45ZGj+XxHyCeL/5wBLuAxQbIybqEe2+pLkhN5sRg8ta4kys38SWvb"

# Kraken Demo API URL
API_URL = "https://demo-futures.kraken.com"

# Generate the signature
def generate_signature(url_path, data, secret):
    post_data = "&".join(f"{key}={value}" for key, value in data.items())  # Convert dict to query string
    encoded = (str(data["nonce"]) + post_data).encode('utf-8')  # Encode the nonce + post data
    message = url_path.encode('utf-8') + hashlib.sha256(encoded).digest()
    
    secret = base64.b64decode(secret)
    signature = hmac.new(secret, message, hashlib.sha512)
    return base64.b64encode(signature.digest())

# Make an authenticated request
def kraken_request(endpoint, data, method="GET"):
    url_path = f"/derivatives/api/v3/{endpoint}"
    headers = {
        "API-Key": API_KEY,
        "API-Sign": generate_signature(url_path, data, API_SECRET)
    }
    url = f"{API_URL}{url_path}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=data)
    else:
        raise ValueError("Invalid HTTP method specified")

    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    return response.json()

# Fetch open positions
def get_open_positions():
    nonce = int(time.time() * 1000)
    data = {
        "nonce": nonce
    }
    return kraken_request("openpositions", data, method="GET")

# Call the function
if __name__ == "__main__":
    try:
        positions = get_open_positions()
        print("Open Positions:", positions)
    except Exception as e:
        print("Error:", e)
