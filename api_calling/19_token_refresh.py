"""
📘 TOPIC 19: Token Refresh — Keeping Sessions Alive
==================================================
Access tokens expire for security. A long-lived refresh token lets
the client get new access tokens without asking the user to log in.

Flow:
  access_token  → short-lived (15 min - 1 hr), sent with every request
  refresh_token → long-lived (days), only sent to /token endpoint
"""

import requests
import time

TOKEN_URL = "https://httpbin.org/post"  # demo echo endpoint


# ─────────────────────────────────────────────
# 1. Simulate token lifecycle
# ─────────────────────────────────────────────
class TokenManager:
    def __init__(self, access_ttl=5):
        self.access_token = "acc_0001"
        self.refresh_token = "ref_0001"
        self.expires_at = time.time() + access_ttl

    def is_expired(self):
        return time.time() > self.expires_at

    def refresh(self):
        print("    → POST /token {grant_type: refresh_token}")
        r = requests.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        })
        print(f"    Status: {r.status_code}")
        # in reality the response contains fresh tokens
        self.access_token = "acc_0002"
        self.expires_at = time.time() + 5
        return self.access_token


def simulate_lifecycle():
    print("\n── Token Lifecycle ──────────────────")
    tm = TokenManager(access_ttl=2)
    print(f"  Access token active: {tm.access_token}")
    time.sleep(2.2)  # let it expire
    print(f"  Expired? {tm.is_expired()}")
    new_token = tm.refresh()
    print(f"  Refreshed to: {new_token}")


# ─────────────────────────────────────────────
# 2. Auto-refresh on 401
# ─────────────────────────────────────────────
class AutoRefreshClient:
    """Retries a 401 response once after refreshing the token."""

    def __init__(self):
        self.access_token = "expired_token"
        self.attempts = 0

    def request(self):
        self.attempts += 1
        if self.attempts == 1:
            print("    → First call → 401 Unauthorized")
            return 401
        print("    → Second call → 200 OK (fresh token)")
        return 200


def auto_refresh_on_401():
    print("\n── Auto-refresh on 401 ──────────────")
    client = AutoRefreshClient()
    status = client.request()
    if status == 401:
        print("    Refreshing token...")
        client.access_token = "fresh_token"
        status = client.request()
    print(f"  Final status: {status}")


# ─────────────────────────────────────────────
# 3. Refresh token best practices
# ─────────────────────────────────────────────
def refresh_best_practices():
    print("\n── Best Practices ───────────────────")
    tips = [
        "Store refresh token securely (HttpOnly cookie / secure vault)",
        "Rotate refresh tokens: each use issues a new one",
        "Revoke refresh tokens on logout or password change",
        "Detect reuse → treat as token theft",
    ]
    for t in tips:
        print(f"  • {t}")


if __name__ == "__main__":
    print("=" * 55)
    print("  TOKEN REFRESH: keeping sessions alive")
    print("=" * 55)
    simulate_lifecycle()
    auto_refresh_on_401()
    refresh_best_practices()
    print("\nToken refresh demos complete.")