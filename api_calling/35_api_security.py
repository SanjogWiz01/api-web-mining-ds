"""
📘 TOPIC 35: API Security — Signatures & HMAC
============================================
Beyond API keys, many APIs require requests to be *signed*
so nobody can tamper with them in transit.

Signature flows:
  HMAC-SHA256 over (timestamp + method + path + body)
  Send signature + timestamp in headers
  Server recomputes and compares
"""

import requests
import hmac
import hashlib
import time
import json

API_SECRET = "shared-signing-secret"
BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Build an HMAC signature
# ─────────────────────────────────────────────
def sign_request(method: str, path: str, body: dict = None,
                 timestamp: str = None) -> dict:
    ts = timestamp or str(int(time.time()))
    body_str = json.dumps(body, separators=(",", ":")) if body else ""
    message = f"{method}|{path}|{ts}|{body_str}"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {"X-Timestamp": ts, "X-Signature": signature, "message": message}


def build_signed_headers():
    print("\n── HMAC Signature ───────────────────")
    headers = sign_request("GET", "/posts/1")
    print(f"  Message      : {headers['message']}")
    print(f"  X-Timestamp  : {headers['X-Timestamp']}")
    print(f"  X-Signature  : {headers['X-Signature'][:32]}...")


# ─────────────────────────────────────────────
# 2. Send a signed request
# ─────────────────────────────────────────────
def send_signed():
    print("\n── Send Signed Request ──────────────")
    signed = sign_request("GET", "/posts/1")
    headers = {"X-Timestamp": signed["X-Timestamp"], "X-Signature": signed["X-Signature"]}
    r = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    print(f"  Status: {r.status_code}")
    print(f"  Signature sent: {headers['X-Signature'][:24]}...")


# ─────────────────────────────────────────────
# 3. Verify server-side (illustration)
# ─────────────────────────────────────────────
def verify_server_side():
    print("\n── Server-Side Verification ─────────")
    signed = sign_request("POST", "/posts", {"title": "x"}, timestamp="1700000000")
    recomputed = sign_request("POST", "/posts", {"title": "x"}, timestamp="1700000000")
    ok = hmac.compare_digest(signed["X-Signature"], recomputed["X-Signature"])
    print(f"  Recompute signature → match? {ok}")
    print("  Also reject if timestamp is too old (replay protection).")


# ─────────────────────────────────────────────
# 4. Security checklist
# ─────────────────────────────────────────────
def security_checklist():
    print("\n── Security Checklist ───────────────")
    items = [
        "Sign with a secret stored in env (never in code)",
        "Include a timestamp to prevent replay attacks",
        "Use HTTPS everywhere",
        "Rotate secrets regularly",
    ]
    for i in items:
        print(f"  ☐ {i}")


if __name__ == "__main__":
    print("=" * 55)
    print("  SECURITY: HMAC signatures")
    print("=" * 55)
    build_signed_headers()
    send_signed()
    verify_server_side()
    security_checklist()
    print("\nSecurity demos complete.")