"""
📘 TOPIC 4: Request Headers
============================
Headers are key-value metadata sent with every HTTP request/response.
The most important request headers:

  Content-Type   → What format data you are SENDING (e.g., application/json)
  Accept         → What format you want to RECEIVE   (e.g., application/json)
  Authorization  → Credentials for authentication    (e.g., Bearer <token>)
  User-Agent     → Identifies the client making the request
  X-Request-ID   → Custom ID for request tracing (useful in logging)
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def show_request_headers():
    print("=" * 50)
    print("  REQUEST HEADERS: Content-Type, Authorization")
    print("=" * 50)

    # ── Standard JSON Headers ─────────────────
    print("\n── Standard JSON Headers ────────────")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "MyAPIClient/1.0 (Python requests)",
    }
    response = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    print(f"Status Code : {response.status_code}")
    print(f"Headers Sent:")
    for k, v in headers.items():
        print(f"  {k}: {v}")

    # ── Inspect Response Headers ──────────────
    print("\n── Response Headers from Server ─────")
    for key, value in list(response.headers.items())[:8]:
        print(f"  {key}: {value}")

    # ── POST with Content-Type ────────────────
    print("\n── POST with application/json ───────")
    payload = {"title": "Header Demo", "body": "Content-Type matters!", "userId": 1}
    headers_post = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer DEMO_TOKEN_123",
        "X-Request-ID": "req-20240801-001",
    }
    r = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers_post)
    print(f"Status Code  : {r.status_code}")
    print(f"Content-Type : {r.headers.get('Content-Type', 'N/A')}")
    print(f"Created Post : {r.json()}")

    # ── Common Header Reference ───────────────
    print("\n── Common Headers Reference ─────────")
    common_headers = {
        "Content-Type: application/json":        "Sending JSON body",
        "Content-Type: multipart/form-data":     "Sending file uploads",
        "Accept: application/json":              "Expect JSON back",
        "Authorization: Bearer <token>":         "OAuth2/JWT auth",
        "Authorization: Basic <base64>":         "Basic auth",
        "X-API-Key: <key>":                      "API key auth",
        "Cache-Control: no-cache":               "Bypass cache",
        "User-Agent: MyApp/1.0":                 "Identify your client",
    }
    for header, purpose in common_headers.items():
        print(f"  {header}")
        print(f"    → {purpose}")

    print("\nHeader demos complete.")


if __name__ == "__main__":
    show_request_headers()
