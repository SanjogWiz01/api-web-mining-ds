"""Practice file: JWT and OAuth2 in Python.

Covers:
  - decoding a JWT (header.payload.signature) without a library
  - verifying + decoding with PyJWT
  - OAuth2 client credentials + refresh token flows with requests

Run:  python 16_jwt_oauth2.py
"""

import base64
import json
import time

import requests


def b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


def decode_jwt_manually(token: str) -> tuple[dict, dict]:
    """Decode JWT by hand (no verification - demo only)."""
    header, payload, _ = token.split(".")
    return (
        json.loads(b64url_decode(header)),
        json.loads(b64url_decode(payload)),
    )


def demo_manual_jwt() -> None:
    print("== manual JWT decode ==")
    # HS256 token signed with secret "secret" (header.payload.signature)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"sub": "42", "name": "Sanjog", "exp": int(time.time()) + 3600}
    # build a real token using PyJWT if available, else fake it:
    try:
        import jwt as pyjwt
        token = pyjwt.encode(payload, "secret", algorithm="HS256")
    except ImportError:
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0MiIsIm5hbWUiOiJTdW4ifQ.m4XkH-XYz0qv9NDtA6YlD0_3aD4pG6oW2qSdZbbPz-0"

    h, p = decode_jwt_manually(token)
    print(f"  header={h}")
    print(f"  payload sub={p['sub']}, name={p['name']}")


def demo_pyjwt_verify() -> None:
    print("== verify + decode with PyJWT ==")
    try:
        import jwt as pyjwt
    except ImportError:
        print("  PyJWT not installed; pip install pyjwt")
        return

    token = pyjwt.encode({"sub": "42", "exp": int(time.time()) + 3600}, "s3cret", algorithm="HS256")

    decoded = pyjwt.decode(token, "s3cret", algorithms=["HS256"])
    print(f"  verified, sub={decoded['sub']}")

    # expired token should raise ExpiredSignatureError
    expired = pyjwt.encode({"sub": "1", "exp": int(time.time()) - 10}, "s3cret", algorithm="HS256")
    try:
        pyjwt.decode(expired, "s3cret", algorithms=["HS256"])
    except pyjwt.ExpiredSignatureError:
        print("  expired token correctly rejected")


def demo_oauth_client_credentials() -> None:
    print("== OAuth2 client credentials flow ==")
    # Real providers look like:
    #   POST /oauth/token  {grant_type, client_id, client_secret, scope}
    # Demo against a public mock is not available, so we show the shape.
    payload = {
        "grant_type": "client_credentials",
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "scope": "read write",
    }
    r = requests.post(
        "https://example.invalid/oauth/token",
        data=payload,
        timeout=(3, 10),
    )
    print(f"  (expected to fail - demo shape) status={r.status_code}")


class TokenManager:
    """Caches an access token and refreshes it automatically."""

    def __init__(self, client_id: str, client_secret: str, token_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = token_url
        self.access_token: str | None = None
        self.refresh_token: str | None = None
        self.expires_at: float = 0.0

    def get_token(self, refresh: bool = False) -> str:
        if self.access_token and time.time() < self.expires_at - 60 and not refresh:
            return self.access_token

        payload = {
            "grant_type": "refresh_token" if refresh and self.refresh_token else "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.refresh_token:
            payload["refresh_token"] = self.refresh_token

        r = requests.post(self.token_url, data=payload, timeout=(3, 10))
        r.raise_for_status()
        data = r.json()
        self.access_token = data["access_token"]
        self.refresh_token = data.get("refresh_token", self.refresh_token)
        self.expires_at = time.time() + int(data.get("expires_in", 3600))
        return self.access_token


def demo_token_manager() -> None:
    print("== TokenManager (shape only) ==")
    tm = TokenManager("cid", "csecret", "https://example.invalid/oauth/token")
    try:
        tm.get_token()
    except requests.RequestException:
        print("  network call not available in demo - logic shown only")


if __name__ == "__main__":
    demo_manual_jwt()
    demo_pyjwt_verify()
    demo_oauth_client_credentials()
    demo_token_manager()
