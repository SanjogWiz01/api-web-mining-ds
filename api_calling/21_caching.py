"""
📘 TOPIC 21: Caching — ETag & Conditional Requests
=================================================
Caching avoids re-downloading unchanged data and cuts API costs.

HTTP conditional headers:
  If-None-Match: <etag>  → 304 Not Modified if unchanged
  If-Modified-Since: <date>

A 304 means "use your cached copy" — no body is sent.
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Inspect cache headers in the response
# ─────────────────────────────────────────────
def inspect_cache_headers():
    print("\n── Cache Headers ────────────────────")
    r = requests.get(f"{BASE_URL}/posts/1")
    print(f"  ETag            : {r.headers.get('ETag', 'n/a')}")
    print(f"  Last-Modified   : {r.headers.get('Last-Modified', 'n/a')}")
    print(f"  Cache-Control   : {r.headers.get('Cache-Control', 'n/a')}")
    print(f"  Age             : {r.headers.get('Age', 'n/a')}")


# ─────────────────────────────────────────────
# 2. Conditional request with If-None-Match
# ─────────────────────────────────────────────
def conditional_request():
    print("\n── Conditional Request (ETag) ───────")
    first = requests.get(f"{BASE_URL}/posts/1")
    etag = first.headers.get("ETag")
    print(f"  First call  → 200 ({len(first.content)} bytes) ETag={etag}")

    if etag:
        second = requests.get(f"{BASE_URL}/posts/1", headers={"If-None-Match": etag})
        print(f"  Second call → {second.status_code} ({len(second.content)} bytes)")
        if second.status_code == 304:
            print("  → 304 Not Modified: reuse the cached copy!")
        else:
            print("  → Server returned fresh data")


# ─────────────────────────────────────────────
# 3. Manual client-side cache
# ─────────────────────────────────────────────
class SimpleCache:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value


def client_side_cache():
    print("\n── Client-Side Cache ────────────────")
    cache = SimpleCache()
    url = f"{BASE_URL}/users/1"
    cache.set(url, requests.get(url).json())  # prime the cache
    print(f"  Cache miss → fetched & stored: {url}")
    print(f"  Cache hit  → returned from memory: {cache.get(url)['name']}")


# ─────────────────────────────────────────────
# 4. Respect Cache-Control
# ─────────────────────────────────────────────
def cache_control_rules():
    print("\n── Cache-Control Semantics ──────────")
    rules = [
        ("max-age=3600", "Store for up to 1 hour"),
        ("no-cache", "Always revalidate before reuse"),
        ("no-store", "Never store (sensitive data)"),
        ("private", "Only for the single user's browser"),
    ]
    for header, meaning in rules:
        print(f"  Cache-Control: {header:<14} → {meaning}")


if __name__ == "__main__":
    print("=" * 55)
    print("  CACHING: ETag + conditional requests")
    print("=" * 55)
    inspect_cache_headers()
    conditional_request()
    client_side_cache()
    cache_control_rules()
    print("\nCaching demos complete.")