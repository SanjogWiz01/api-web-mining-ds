"""
📘 TOPIC 20: Batch Requests — Fewer Round Trips
==============================================
Batching groups many operations into one HTTP request to cut
latency and rate-limit usage.

Patterns:
  Endpoint batch  → POST /batch with an array of operations
  jsonrpc         → single endpoint, method + params per call
  GraphQL         → one query for many resources (see topic 25)
  Parallel client → fire independent requests concurrently (topic 24)
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Simulate a batch endpoint payload
# ─────────────────────────────────────────────
def batch_endpoint_payload():
    print("\n── Batch Endpoint Pattern ───────────")
    batch = [
        {"method": "GET", "path": "/posts/1"},
        {"method": "GET", "path": "/users/1"},
        {"method": "GET", "path": "/comments?postId=1"},
    ]
    print(f"  Batch request body ({len(batch)} ops):")
    print("  " + json.dumps(batch, indent=2))


# ─────────────────────────────────────────────
# 2. Sequential vs batch comparison (illustration)
# ─────────────────────────────────────────────
def compare_latency():
    print("\n── Sequential vs Batch ──────────────")
    urls = [
        f"{BASE_URL}/posts/1",
        f"{BASE_URL}/users/1",
        f"{BASE_URL}/comments",
    ]
    print("  Sequential: 3 separate HTTP round trips")
    for u in urls:
        r = requests.get(u)
        print(f"    GET {u.split('typicode.com')[-1]} → {r.status_code} ({len(r.content)} bytes)")
    print("  Batch     : 1 HTTP round trip with 3 operations inside")


# ─────────────────────────────────────────────
# 3. JSON-RPC style batching
# ─────────────────────────────────────────────
def jsonrpc_batch():
    print("\n── JSON-RPC Style ───────────────────")
    batch = [
        {"jsonrpc": "2.0", "method": "getPost", "params": {"id": 1}, "id": 1},
        {"jsonrpc": "2.0", "method": "getUser", "params": {"id": 1}, "id": 2},
    ]
    r = requests.post(f"{BASE_URL}/posts", json=batch)  # demo echo only
    print(f"  Payload with ids for correlation: {[op['id'] for op in batch]}")
    print(f"  Status: {r.status_code}")


# ─────────────────────────────────────────────
# 4. Caveats
# ─────────────────────────────────────────────
def batch_caveats():
    print("\n── Caveats ───────────────────────────")
    tips = [
        "Batch size limits (e.g. max 50 ops)",
        "Partial failure: handle per-item status codes",
        "Auth applies to the whole batch",
        "Large batches can be slower than parallel individual calls",
    ]
    for t in tips:
        print(f"  • {t}")


if __name__ == "__main__":
    print("=" * 55)
    print("  BATCH REQUESTS: fewer round trips")
    print("=" * 55)
    batch_endpoint_payload()
    compare_latency()
    jsonrpc_batch()
    batch_caveats()
    print("\nBatch request demos complete.")