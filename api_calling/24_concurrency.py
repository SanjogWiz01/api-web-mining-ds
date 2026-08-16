"""
📘 TOPIC 24: Concurrency — asyncio & Thread Pools
===============================================
Sequential API calls waste time waiting on the network.
Concurrency lets many requests be in flight at once.

Tools:
  requests + ThreadPoolExecutor → simple blocking style
  httpx / aiohttp + asyncio     → true async, non-blocking
"""

import requests
import time
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Sequential baseline
# ─────────────────────────────────────────────
def sequential_fetch(n=8):
    start = time.perf_counter()
    results = [requests.get(f"{BASE_URL}/posts/{i}").json() for i in range(1, n + 1)]
    elapsed = time.perf_counter() - start
    print(f"  Sequential: {n} posts in {elapsed:.2f}s")
    return elapsed, results


# ─────────────────────────────────────────────
# 2. Thread pool concurrency
# ─────────────────────────────────────────────
def concurrent_fetch(n=8, workers=8):
    def fetch(i):
        return requests.get(f"{BASE_URL}/posts/{i}").json()

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(fetch, range(1, n + 1)))
    elapsed = time.perf_counter() - start
    print(f"  Concurrent: {n} posts in {elapsed:.2f}s ({workers} workers)")
    return elapsed, results


def compare_speed():
    print("\n── Sequential vs Concurrent ─────────")
    seq_time, _ = sequential_fetch()
    con_time, results = concurrent_fetch()
    speedup = seq_time / con_time if con_time else 0
    print(f"  Speedup: {speedup:.1f}x")
    print(f"  First post title: {results[0]['title'][:45]}")


# ─────────────────────────────────────────────
# 3. Async with httpx (needs `pip install httpx`)
# ─────────────────────────────────────────────
def async_demo():
    print("\n── Async (httpx) ────────────────────")
    try:
        import httpx
        import asyncio

        async def fetch_all():
            async with httpx.AsyncClient() as client:
                tasks = [client.get(f"{BASE_URL}/posts/{i}") for i in range(1, 9)]
                responses = await asyncio.gather(*tasks)
                return [r.json() for r in responses]

        start = time.perf_counter()
        data = asyncio.run(fetch_all())
        elapsed = time.perf_counter() - start
        print(f"  Fetched {len(data)} posts in {elapsed:.2f}s")
    except ImportError:
        print("  httpx not installed — skipping (pip install httpx)")


# ─────────────────────────────────────────────
# 4. Semaphore to limit concurrency (politeness)
# ─────────────────────────────────────────────
def rate_limited_concurrency():
    print("\n── Rate-Limited Concurrency ─────────")
    print("  Use a Semaphore to cap in-flight requests:")
    print("    sem = asyncio.Semaphore(5)   # max 5 concurrent")
    print("  Respect the API's rate limits while staying fast.")


if __name__ == "__main__":
    print("=" * 55)
    print("  CONCURRENCY: parallel API calls")
    print("=" * 55)
    compare_speed()
    async_demo()
    rate_limited_concurrency()
    print("\nConcurrency demos complete.")