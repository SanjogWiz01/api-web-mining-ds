"""
📘 TOPIC 37: API Documentation Driven Development
================================================
Great APIs ship with great docs. Building against them starts
by reading the docs, not the network tab.

Doc resources:
  OpenAPI / Swagger UI → interactive, run requests from browser
  Postman collections   → ready-made request examples
  Changelogs            → know what changed & deprecations
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Enumerate what the docs told us
# ─────────────────────────────────────────────
def doc_inventory():
    print("\n── Doc Inventory ────────────────────")
    endpoints = [
        ("GET", "/posts", "List posts"),
        ("GET", "/posts/1", "Single post"),
        ("GET", "/posts/1/comments", "Comments of a post"),
        ("POST", "/posts", "Create a post"),
        ("GET", "/users", "List users"),
    ]
    for method, path, desc in endpoints:
        print(f"  {method:<5} {path:<18} {desc}")


# ─────────────────────────────────────────────
# 2. Try endpoints listed in the docs
# ─────────────────────────────────────────────
def try_documented():
    print("\n── Try Documented Endpoints ─────────")
    for method, path, _ in [("GET", "/posts/1/comments", None), ("GET", "/users", None)]:
        r = requests.request(method, f"{BASE_URL}{path}", params={"_limit": 1})
        print(f"  {method} {path} → {r.status_code}")
    print("  Docs said fields: postId, id, name, email, body")


# ─────────────────────────────────────────────
# 3. Changelog & deprecations
# ─────────────────────────────────────────────
def changelog():
    print("\n── Changelog & Deprecations ─────────")
    print("  • Watch the changelog for breaking changes")
    print("  • Subscribe to Sunset / Deprecation headers")
    print("  • Pin the API version you integrate against")


# ─────────────────────────────────────────────
# 4. Docs-first checklist
# ─────────────────────────────────────────────
def docs_checklist():
    print("\n── Docs-First Checklist ─────────────")
    items = [
        "Base URL & auth method",
        "Rate limits & pagination",
        "Required headers & content types",
        "Error response shape",
        "Example requests (copy-paste friendly)",
    ]
    for i in items:
        print(f"  ☐ {i}")


if __name__ == "__main__":
    print("=" * 55)
    print("  DOC-DRIVEN DEVELOPMENT: read first")
    print("=" * 55)
    doc_inventory()
    try_documented()
    changelog()
    docs_checklist()
    print("\nDoc-driven demos complete.")