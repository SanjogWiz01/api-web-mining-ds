"""
📘 TOPIC 29: Rate Limit Headers — Reading the Meter
==================================================
Well-behaved APIs tell you your current rate usage via headers.
Learn to read them and slow down BEFORE you get a 429.

Common headers:
  X-RateLimit-Limit      → max requests allowed per window
  X-RateLimit-Remaining  → requests left in this window
  X-RateLimit-Reset      → seconds until the window resets
  Retry-After            → seconds to wait before retrying
"""

import requests
import time

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Inspect rate-limit headers (if present)
# ─────────────────────────────────────────────
def inspect_headers():
    print("\n── Rate Limit Headers ───────────────")
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 1})
    headers = r.headers
    candidates = [
        "X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset",
        "RateLimit-Limit", "RateLimit-Remaining", "RateLimit-Reset",
        "Retry-After", "X-RateLimit-RetryAfter",
    ]
    found = False
    for h in candidates:
        if h in headers:
            found = True
            print(f"  {h:<26} {headers[h]}")
    if not found:
        print("  (This test API does not send rate-limit headers.)")
        print("  Real APIs usually send them — see above list.")


# ─────────────────────────────────────────────
# 2. Polite throttling client
# ─────────────────────────────────────────────
class PoliteClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.remaining = None
        self.reset = None

    def update_from_headers(self, headers):
        self.remaining = headers.get("X-RateLimit-Remaining")
        self.reset = headers.get("X-RateLimit-Reset")

    def get(self, path):
        r = requests.get(f"{self.base_url}{path}")
        self.update_from_headers(r.headers)
        print(f"  GET {path} → {r.status_code} | remaining={self.remaining} reset={self.reset}")
        if self.remaining is not None and int(self.remaining) <= 2:
            print("    ⚠ Low quota — consider pausing!")
        return r


def polite_client_demo():
    print("\n── Polite Throttling Client ─────────")
    client = PoliteClient(BASE_URL)
    for i in range(1, 4):
        client.get(f"/posts/{i}")
        time.sleep(0.2)


# ─────────────────────────────────────────────
# 3. Handle 429 with Retry-After
# ─────────────────────────────────────────────
def handle_429():
    print("\n── Handling 429 ─────────────────────")
    print("  On 429 Too Many Requests:")
    retry_after = "2"
    wait = float(retry_after) if retry_after else 1.0
    print(f"    Read Retry-After header → wait {wait}s")
    print("    Or back off exponentially + jitter")
    print("    Never retry 429 in a tight loop")


# ─────────────────────────────────────────────
# 4. Play nice — ethical rate limiting
# ─────────────────────────────────────────────
def ethics():
    print("\n── Play Nice ────────────────────────")
    tips = [
        "Stay under documented limits",
        "Back off when remaining quota is low",
        "Cache responses you call repeatedly",
        "Batch instead of hammering",
    ]
    for t in tips:
        print(f"  • {t}")


if __name__ == "__main__":
    print("=" * 55)
    print("  RATE LIMIT HEADERS: read the meter")
    print("=" * 55)
    inspect_headers()
    polite_client_demo()
    handle_429()
    ethics()
    print("\nRate limit demos complete.")