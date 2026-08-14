"""
📘 TOPIC 6: Rate Limits — Respect API Quotas
=============================================
Rate limiting controls how many API requests you can make in a timeframe.
Exceeding limits results in a 429 Too Many Requests response.

Common rate limit headers returned by APIs:
  X-RateLimit-Limit     → Max requests allowed per window
  X-RateLimit-Remaining → Requests remaining in current window
  X-RateLimit-Reset     → Unix timestamp when the window resets
  Retry-After           → Seconds to wait before retrying (after 429)

Strategies:
  - Exponential Backoff  → Wait 1s, 2s, 4s, 8s... on repeated failures
  - Request Queuing      → Batch calls instead of firing all at once
  - Caching              → Store results to avoid redundant calls
  - Throttling           → Manually sleep between requests
"""

import requests
import time
import random


BASE_URL = "https://jsonplaceholder.typicode.com"


def inspect_rate_limit_headers(response: requests.Response):
    """Check and display any rate-limit headers in the response."""
    rate_headers = {
        "X-RateLimit-Limit": "Max requests",
        "X-RateLimit-Remaining": "Requests left",
        "X-RateLimit-Reset": "Reset timestamp",
        "Retry-After": "Retry after (seconds)",
        "X-RateLimit-Used": "Requests used",
    }
    found = False
    for header, desc in rate_headers.items():
        value = response.headers.get(header)
        if value:
            print(f"  {header}: {value} ({desc})")
            found = True
    if not found:
        print("  (No rate-limit headers in this response — API may not expose them)")


def exponential_backoff_request(url: str, max_retries: int = 5) -> requests.Response | None:
    """Retry a request with exponential backoff on 429 or 5xx errors."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 429:
                wait = response.headers.get("Retry-After", 2 ** attempt)
                print(f"  [429] Rate limited. Waiting {wait}s before retry {attempt + 1}...")
                time.sleep(float(wait))
                continue
            if response.status_code >= 500:
                wait = (2 ** attempt) + random.uniform(0, 1)  # jitter
                print(f"  [{response.status_code}] Server error. Backing off {wait:.1f}s...")
                time.sleep(wait)
                continue
            return response
        except requests.exceptions.ConnectionError:
            wait = 2 ** attempt
            print(f"  Connection error. Retry {attempt + 1} in {wait}s...")
            time.sleep(wait)
    return None


def throttled_batch_requests(post_ids: list, delay: float = 0.3):
    """Fetch multiple resources with a delay between requests to avoid rate limits."""
    print(f"\n── Throttled Batch ({delay}s between calls) ─")
    results = []
    for pid in post_ids:
        r = requests.get(f"{BASE_URL}/posts/{pid}")
        title = r.json().get("title", "N/A")[:40]
        print(f"  Post {pid:>3}: [{r.status_code}] {title}...")
        results.append(r.json())
        time.sleep(delay)  # polite delay
    return results


def demo_rate_limits():
    print("=" * 55)
    print("  RATE LIMITS: Backoff, Throttling, Header Inspection")
    print("=" * 55)

    # ── Check Headers on Normal Response ─────
    print("\n── Rate Limit Headers on Response ───")
    r = requests.get(f"{BASE_URL}/posts/1")
    inspect_rate_limit_headers(r)

    # ── Exponential Backoff ───────────────────
    print("\n── Exponential Backoff Request ──────")
    result = exponential_backoff_request(f"{BASE_URL}/posts/2")
    if result:
        print(f"  Success [{result.status_code}]: {result.json().get('title', '')[:50]}")
    else:
        print("  All retries exhausted.")

    # ── Throttled Batch ───────────────────────
    throttled_batch_requests([1, 2, 3, 4, 5], delay=0.2)

    # ── Best Practices Summary ────────────────
    print("\n── Rate Limit Best Practices ────────")
    tips = [
        "Always check X-RateLimit-Remaining before large batch jobs",
        "Implement exponential backoff with random jitter",
        "Cache responses to reduce redundant API calls",
        "Use bulk endpoints when available (e.g., /posts?ids=1,2,3)",
        "Monitor your usage in the API dashboard",
        "Set conservative request intervals in production",
    ]
    for i, tip in enumerate(tips, 1):
        print(f"  {i}. {tip}")

    print("\nRate limit demos complete.")


if __name__ == "__main__":
    demo_rate_limits()
