"""
📘 TOPIC 2: Authentication First
=================================
Most APIs require you to prove who you are before granting access.
Common authentication methods:

  1. API Key       → A simple secret string passed in headers or query params
  2. Bearer Token  → JWT or OAuth2 access token in the Authorization header
  3. Basic Auth    → Base64-encoded username:password (legacy, avoid if possible)
  4. OAuth2        → Full authorization flow with access + refresh tokens
"""

import requests
import base64

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# Method 1: API Key in Query Parameter
# ─────────────────────────────────────────────
def api_key_in_query():
    print("\n── API Key via Query Param ──────────")
    # Example: ?api_key=YOUR_KEY  (e.g., OpenWeatherMap style)
    API_KEY = "YOUR_API_KEY_HERE"
    url = f"https://api.example.com/data"
    # requests.get(url, params={"api_key": API_KEY})
    print(f"Example URL: {url}?api_key={API_KEY}")
    print("Status: Would send key in the URL (not recommended for sensitive keys)")


# ─────────────────────────────────────────────
# Method 2: API Key in Request Header
# ─────────────────────────────────────────────
def api_key_in_header():
    print("\n── API Key via Header ───────────────")
    API_KEY = "YOUR_SECRET_API_KEY"
    headers = {
        "X-API-Key": API_KEY,       # Common header name
        "Content-Type": "application/json",
    }
    # Simulated call — jsonplaceholder ignores extra headers
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    print(f"Status Code : {response.status_code}")
    print(f"Headers Sent: X-API-Key: {API_KEY[:8]}... (truncated for safety)")


# ─────────────────────────────────────────────
# Method 3: Bearer Token (OAuth2 / JWT)
# ─────────────────────────────────────────────
def bearer_token_auth():
    print("\n── Bearer Token Auth ────────────────")
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.FAKE_TOKEN"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    print(f"Status Code     : {response.status_code}")
    print(f"Authorization   : Bearer {TOKEN[:30]}...")
    print(f"Response Title  : {response.json().get('title', 'N/A')}")


# ─────────────────────────────────────────────
# Method 4: Basic Authentication
# ─────────────────────────────────────────────
def basic_auth():
    print("\n── Basic Auth ───────────────────────")
    username = "myuser"
    password = "mypassword"

    # requests handles encoding automatically
    response = requests.get(
        f"{BASE_URL}/posts/1",
        auth=(username, password)
    )
    # Manual encoding for demonstration:
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    print(f"Status Code       : {response.status_code}")
    print(f"Encoded Credential: Basic {credentials}")


if __name__ == "__main__":
    print("=" * 50)
    print("  AUTHENTICATION: API Keys, Tokens, OAuth")
    print("=" * 50)
    api_key_in_query()
    api_key_in_header()
    bearer_token_auth()
    basic_auth()
    print("\nAuthentication demos complete.")
    print("\nSECURITY REMINDER: Never hardcode real keys in production code!")
