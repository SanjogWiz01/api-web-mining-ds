"""
📘 TOPIC 31: Mock APIs — Develop Without Waiting
===============================================
Mocking lets you build against an API before it exists
or when you don't want to hit the real one in tests.

Tools & services:
  JSONPlaceholder      → static fake data (used here)
  httpbin.org          → echoes requests back
  Mock Server / WireMock / Prism → generate from OpenAPI specs
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Fake data endpoints (mocks in the wild)
# ─────────────────────────────────────────────
def fake_data_endpoints():
    print("\n── Fake Data Endpoints ──────────────")
    for path in ("/posts/1", "/users/1", "/albums/1"):
        r = requests.get(f"{BASE_URL}{path}")
        print(f"  GET {path} → {r.status_code} ({len(r.content)}B)")


# ─────────────────────────────────────────────
# 2. In-memory mock client
# ─────────────────────────────────────────────
class MockClient:
    """A tiny in-memory mock that behaves like a REST API."""

    def __init__(self, initial_data):
        self.data = initial_data

    def get(self, key):
        return self.data.get(key)

    def create(self, key, item):
        item["id"] = len(self.data.get(key, [])) + 1
        self.data.setdefault(key, []).append(item)
        return item


def in_memory_mock():
    print("\n── In-Memory Mock ───────────────────")
    mock = MockClient({"posts": [{"id": 1, "title": "Mock post"}]})
    created = mock.create("posts", {"title": "New via mock"})
    print(f"  Mock GET  → {mock.get('posts')}")
    print(f"  Mock POST → created {created}")


# ─────────────────────────────────────────────
# 3. httpbin echo for request inspection
# ─────────────────────────────────────────────
def httpbin_echo():
    print("\n── httpbin Echo ─────────────────────")
    r = requests.post("https://httpbin.org/post",
                      json={"hello": "world"},
                      headers={"X-Custom": "abc"})
    data = r.json()
    print(f"  Echoed JSON : {data.get('json')}")
    print(f"  Echoed X-Custom: {data.get('headers', {}).get('X-Custom')}")


# ─────────────────────────────────────────────
# 4. When to mock vs use real API
# ─────────────────────────────────────────────
def mock_vs_real():
    print("\n── Mock vs Real ─────────────────────")
    comparison = [
        ("Mock", "Fast, deterministic, free, no rate limits"),
        ("     ", "Risk: won't catch real integration bugs"),
        ("Real", "True behavior, catches contract drift"),
        ("     ", "Slower, cost, rate limits"),
    ]
    for label, text in comparison:
        print(f"  {label:<5} {text}")
    print("  Best: mock in unit tests, real in integration tests.")


if __name__ == "__main__":
    print("=" * 55)
    print("  MOCK APIS: develop without waiting")
    print("=" * 55)
    fake_data_endpoints()
    in_memory_mock()
    httpbin_echo()
    mock_vs_real()
    print("\nMock API demos complete.")