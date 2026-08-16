"""
📘 TOPIC 17: OAuth 2.0 — Authorization Flows
===========================================
OAuth 2.0 lets an app get access to a user's data on another service
without sharing the password.

Main grant types:
  Authorization Code → for web apps (server-side, most secure)
  PKCE              → for mobile/public clients
  Client Credentials → for machine-to-machine (no user)
  Password Grant    → legacy, discouraged
"""

import requests
import base64

TOKEN_URL = "https://httpbin.org/post"  # demo echo endpoint


# ─────────────────────────────────────────────
# 1. Authorization Code flow (steps)
# ─────────────────────────────────────────────
def authorization_code_flow():
    print("\n── Authorization Code Flow ──────────")
    steps = [
        ("1", "Redirect user to authorize URL with client_id + scopes"),
        ("2", "User logs in & grants consent"),
        ("3", "Service redirects back with ?code=AUTH_CODE"),
        ("4", "Server exchanges code + client_secret for tokens"),
        ("5", "Receive access_token + refresh_token"),
    ]
    for num, step in steps:
        print(f"  Step {num}: {step}")


# ─────────────────────────────────────────────
# 2. Client Credentials flow (machine-to-machine)
# ─────────────────────────────────────────────
def client_credentials():
    print("\n── Client Credentials ───────────────")
    payload = {
        "grant_type": "client_credentials",
        "client_id": "demo_client",
        "client_secret": "demo_secret",
    }
    r = requests.post(TOKEN_URL, data=payload)
    print(f"  Status: {r.status_code}")
    print(f"  Request body echo: {r.json().get('form')}")


# ─────────────────────────────────────────────
# 3. Password grant (legacy)
# ─────────────────────────────────────────────
def password_grant():
    print("\n── Password Grant (legacy) ──────────")
    payload = {
        "grant_type": "password",
        "username": "alice",
        "password": "hunter2",
    }
    r = requests.post(TOKEN_URL, data=payload)
    print(f"  Status: {r.status_code}")
    print(f"  Request body echo: {r.json().get('form')}")


# ─────────────────────────────────────────────
# 4. Use access token in Authorization header
# ─────────────────────────────────────────────
def use_access_token():
    print("\n── Using Access Token ───────────────")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo.token"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://jsonplaceholder.typicode.com/users/1", headers=headers)
    print(f"  Status: {r.status_code}")
    print(f"  Auth header sent: {r.request.headers.get('Authorization')[:30]}...")


if __name__ == "__main__":
    print("=" * 55)
    print("  OAUTH 2.0: authorization flows")
    print("=" * 55)
    authorization_code_flow()
    client_credentials()
    password_grant()
    use_access_token()
    print("\nOAuth 2.0 demos complete.")