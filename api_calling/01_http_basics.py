"""
📘 TOPIC 1: HTTP Basics — GET, POST, PUT, DELETE
=================================================
HTTP (HyperText Transfer Protocol) is the foundation of web communication.
The four core methods define how we interact with resources on a server.

    GET    → Read / Retrieve data        (safe, idempotent)
    POST   → Create new data             (not idempotent)
    PUT    → Update/Replace existing     (idempotent)
    DELETE → Remove a resource           (idempotent)

We use the `requests` library in Python to make HTTP calls.
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"  # Free fake REST API for testing


# ─────────────────────────────────────────────
# 1. GET — Retrieve a list of posts
# ─────────────────────────────────────────────
def demo_get():
    print("\n── GET Request ──────────────────────")
    response = requests.get(f"{BASE_URL}/posts", params={"_limit": 3})
    print(f"Status Code : {response.status_code}")
    print(f"URL Called  : {response.url}")
    posts = response.json()
    for post in posts:
        print(f"  [{post['id']}] {post['title'][:60]}...")


# ─────────────────────────────────────────────
# 2. POST — Create a new post
# ─────────────────────────────────────────────
def demo_post():
    print("\n── POST Request ─────────────────────")
    payload = {
        "title": "Understanding HTTP Methods",
        "body": "GET retrieves, POST creates, PUT updates, DELETE removes.",
        "userId": 1,
    }
    response = requests.post(f"{BASE_URL}/posts", json=payload)
    print(f"Status Code : {response.status_code}")  # 201 Created
    created = response.json()
    print(f"Created Post ID : {created.get('id')}")
    print(f"Title           : {created.get('title')}")


# ─────────────────────────────────────────────
# 3. PUT — Update an existing post entirely
# ─────────────────────────────────────────────
def demo_put():
    print("\n── PUT Request ──────────────────────")
    updated_payload = {
        "id": 1,
        "title": "Updated Title via PUT",
        "body": "This replaces the entire post resource.",
        "userId": 1,
    }
    response = requests.put(f"{BASE_URL}/posts/1", json=updated_payload)
    print(f"Status Code : {response.status_code}")  # 200 OK
    print(f"Updated Data: {response.json()}")


# ─────────────────────────────────────────────
# 4. DELETE — Remove a post
# ─────────────────────────────────────────────
def demo_delete():
    print("\n── DELETE Request ───────────────────")
    response = requests.delete(f"{BASE_URL}/posts/1")
    print(f"Status Code : {response.status_code}")  # 200 OK
    print(f"Response    : {response.json()}")        # {} resource is gone


# ─────────────────────────────────────────────
# Run All Demos
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  HTTP BASICS: GET | POST | PUT | DELETE")
    print("=" * 50)
    demo_get()
    demo_post()
    demo_put()
    demo_delete()
    print("\nAll HTTP method demos complete.")
