"""
📘 TOPIC 23: Retries & Idempotency Keys
======================================
Network calls fail. Retries make clients resilient.
But blindly retrying a POST can create duplicates → use Idempotency-Key.

Backoff strategies:
  Fixed backoff     → wait same time each retry
  Exponential backoff → double the wait each attempt
  Jitter            → add randomness to avoid thundering herd
"""

import requests
import time
import random

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Retry with exponential backoff
# ─────────────────────────────────────────────
def retry_with_backoff(url, attempts=4, base_delay=0.3):
    print(f"\n── Retry with Exponential Backoff ──")
    for attempt in range(1, attempts + 1):
        try:
            r = requests.get(url, timeout=5)
            if r.status_code < 500:
                print(f"  Attempt {attempt}: {r.status_code} — success")
                return r.json()
            raise ConnectionError(f"Server error {r.status_code}")
        except requests.RequestException as e:
            delay = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 0.1)
            print(f"  Attempt {attempt}: failed ({type(e).__name__}) → wait {delay:.2f}s")
            time.sleep(delay)
    print("  Giving up after all retries.")
    return None


def run_retry_demo():
    result = retry_with_backoff(f"{BASE_URL}/posts/1")
    if result:
        print(f"  Retrieved post: {result['title'][:50]}")


# ─────────────────────────────────────────────
# 2. Idempotency key for safe POST retries
# ─────────────────────────────────────────────
def idempotency_key():
    print("\n── Idempotency Key ──────────────────")
    key = "req_9f8e7d6c-1234-4a5b-9c0d-abcdef123456"
    headers = {"Idempotency-Key": key}
    payload = {"title": "Safe Create", "body": "Retried POST is safe", "userId": 1}
    r = requests.post(f"{BASE_URL}/posts", json=payload, headers=headers)
    print(f"  Status: {r.status_code}")
    print(f"  Sent Idempotency-Key: {headers['Idempotency-Key'][:20]}...")
    print("  → Server can deduplicate if this request repeats")


# ─────────────────────────────────────────────
# 3. Which methods should be retried?
# ─────────────────────────────────────────────
def retry_guidance():
    print("\n── Retry Guidance ───────────────────")
    guidance = [
        ("GET / HEAD", "Safe to retry automatically"),
        ("PUT / DELETE", "Idempotent → retry is safe"),
        ("POST (create)", "NOT safe → use Idempotency-Key"),
        ("401", "Do NOT retry — fix auth first"),
    ]
    for method, advice in guidance:
        print(f"  {method:<12} {advice}")


# ─────────────────────────────────────────────
# 4. Standard Retry-After header
# ─────────────────────────────────────────────
def retry_after():
    print("\n── Retry-After Header ───────────────")
    r = requests.get(f"{BASE_URL}/posts/1")
    print(f"  Retry-After: {r.headers.get('Retry-After', 'not set on this API')}")
    print("  → When 429/503, honor Retry-After before retrying")


if __name__ == "__main__":
    print("=" * 55)
    print("  RETRIES: backoff + idempotency keys")
    print("=" * 55)
    run_retry_demo()
    idempotency_key()
    retry_guidance()
    retry_after()
    print("\nRetry demos complete.")