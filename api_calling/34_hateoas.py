"""
📘 TOPIC 34: HATEOAS — Discoverable APIs
========================================
HATEOAS (Hypermedia As The Engine Of Application State) means
API responses carry the links you can follow next.

    { "id": 1, "name": "Alice",
      "links": { "self": "/users/1", "posts": "/users/1/posts" } }

Clients navigate by links instead of hard-coding URLs.
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Self-referencing / navigation links
# ─────────────────────────────────────────────
def self_links():
    print("\n── Self & Related Links ─────────────")
    user = requests.get(f"{BASE_URL}/users/1").json()
    links = {
        "self": f"/users/{user['id']}",
        "posts": f"/users/{user['id']}/posts",
        "albums": f"/users/{user['id']}/albums",
        "todos": f"/users/{user['id']}/todos",
    }
    print("  User response + generated hypermedia links:")
    for rel, href in links.items():
        print(f"    <{rel}> → {href}")


# ─────────────────────────────────────────────
# 2. Follow links dynamically
# ─────────────────────────────────────────────
def follow_links():
    print("\n── Follow Links Dynamically ─────────")
    links = {"posts": f"{BASE_URL}/users/1/posts"}
    r = requests.get(links["posts"], params={"_limit": 2})
    print(f"  Followed <posts> link → {r.status_code}, got {len(r.json())} posts")


# ─────────────────────────────────────────────
# 3. HAL-style payload structure
# ─────────────────────────────────────────────
def hal_payload():
    print("\n── HAL-Style Payload ────────────────")
    payload = {
        "_links": {"self": {"href": "/users/1"}},
        "id": 1,
        "name": "Leanne Graham",
        "_embedded": {"posts": [{"id": 1}, {"id": 2}]},
    }
    print(json.dumps(payload, indent=2))


# ─────────────────────────────────────────────
# 4. Why HATEOAS matters
# ─────────────────────────────────────────────
def why_hateoas():
    print("\n── Why HATEOAS ──────────────────────")
    points = [
        "Server controls navigation → clients survive URL changes",
        "API is self-documenting to machines",
        "Great for long-running workflows",
    ]
    for p in points:
        print(f"  • {p}")


if __name__ == "__main__":
    print("=" * 55)
    print("  HATEOAS: discoverable hypermedia APIs")
    print("=" * 55)
    self_links()
    follow_links()
    hal_payload()
    why_hateoas()
    print("\nHATEOAS demos complete.")