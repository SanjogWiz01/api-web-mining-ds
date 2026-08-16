"""
📘 TOPIC 18: JWT — JSON Web Tokens
=================================
JWT is a compact token format used for stateless authentication.

Structure: header.payload.signature
  header    → algorithm + type
  payload   → claims (sub, exp, iat, role, ...)
  signature → verifies token was not tampered with

Decode JWTs locally with `python -m pip install pyjwt`.
"""

import jwt
import time

SECRET = "demo-secret-key"
ALGO = "HS256"


# ─────────────────────────────────────────────
# 1. Create (encode) a JWT
# ─────────────────────────────────────────────
def create_jwt():
    print("\n── Create JWT ───────────────────────")
    payload = {
        "sub": "user_42",
        "name": "Alice",
        "role": "admin",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,  # 1 hour
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGO)
    print(f"  Token: {token[:70]}...")
    print(f"  Parts: {len(token.split('.'))} (header.payload.signature)")
    return token


# ─────────────────────────────────────────────
# 2. Decode (verify) a JWT
# ─────────────────────────────────────────────
def decode_jwt(token: str):
    print("\n── Decode JWT ───────────────────────")
    decoded = jwt.decode(token, SECRET, algorithms=[ALGO])
    print(f"  Payload: {decoded}")
    print(f"  Subject: {decoded['sub']} | Role: {decoded['role']}")


# ─────────────────────────────────────────────
# 3. Reject tampered / wrong-secret tokens
# ─────────────────────────────────────────────
def tampered_token():
    print("\n── Tampered Token ───────────────────")
    bad_token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyXzQyIiwicm9sZSI6ImFkbWluIn0.WRONG_SIGNATURE"
    try:
        jwt.decode(bad_token, SECRET, algorithms=[ALGO])
        print("  ✗ Should NOT have decoded")
    except jwt.InvalidTokenError as e:
        print(f"  ✓ Correctly rejected: {type(e).__name__}")


# ─────────────────────────────────────────────
# 4. Send JWT as Bearer token
# ─────────────────────────────────────────────
def send_jwt_bearer():
    print("\n── JWT in Authorization header ──────")
    token = create_jwt()
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get("https://jsonplaceholder.typicode.com/posts/1", headers=headers)
    print(f"  Status: {r.status_code}")
    print(f"  Header: {headers['Authorization'][:40]}...")


import requests  # noqa: E402  (used above)


if __name__ == "__main__":
    print("=" * 55)
    print("  JWT: JSON Web Tokens")
    print("=" * 55)
    token = create_jwt()
    decode_jwt(token)
    tampered_token()
    send_jwt_bearer()
    print("\nJWT demos complete.")