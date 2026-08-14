"""
📘 TOPIC 3: Endpoints Matter
=============================
An API endpoint is a specific URL where a resource lives.
It consists of:
  - Base URL  : The root address of the API server
  - Path      : The specific resource path
  - Parameters: Query strings or path variables

Structure:
  https://api.example.com  /users  /42  ?include=profile
  |___ Base URL ___|  |_Path_| |_ID_|  |___Query Param___|
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def demonstrate_endpoints():
    print("=" * 55)
    print("  ENDPOINTS: Base URL, Paths, Path Params, Query Params")
    print("=" * 55)

    # ── Path Variables (Resource ID in URL) ──
    print("\n── Path Variable: /posts/{id} ───────")
    for post_id in [1, 5, 10]:
        endpoint = f"{BASE_URL}/posts/{post_id}"
        r = requests.get(endpoint)
        title = r.json().get("title", "N/A")[:45]
        print(f"  GET {endpoint}  →  [{r.status_code}] {title}...")

    # ── Nested Resource Path ──────────────────
    print("\n── Nested Path: /posts/{id}/comments ─")
    endpoint = f"{BASE_URL}/posts/1/comments"
    r = requests.get(endpoint)
    comments = r.json()
    print(f"  GET {endpoint}")
    print(f"  Status: {r.status_code} | Comments Found: {len(comments)}")
    print(f"  First comment email: {comments[0].get('email', 'N/A')}")

    # ── Query Parameters ──────────────────────
    print("\n── Query Params: /posts?userId=1&_limit=3 ─")
    endpoint = f"{BASE_URL}/posts"
    params = {"userId": 1, "_limit": 3}
    r = requests.get(endpoint, params=params)
    print(f"  Final URL: {r.url}")
    print(f"  Status: {r.status_code} | Posts Returned: {len(r.json())}")

    # ── Different Resource Collections ────────
    print("\n── API Resource Collections ─────────")
    resources = ["posts", "comments", "albums", "photos", "todos", "users"]
    for res in resources:
        r = requests.get(f"{BASE_URL}/{res}", params={"_limit": 1})
        print(f"  /{res:<10} → {r.status_code} | Example: {list(r.json()[0].keys())[:4]}")

    print("\nEndpoint demos complete.")


if __name__ == "__main__":
    demonstrate_endpoints()
