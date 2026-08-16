"""
📘 TOPIC 12: Filtering & Sorting — Query Parameters
===================================================
APIs let you narrow results with query parameters.

Common patterns:
  filter      → ?userId=1&completed=true
  sort        → ?sort=title&order=asc
  search      → ?q=keyword
  projection  → ?fields=id,title

Always read the API docs — every API uses its own convention.
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Filter by a field (userId)
# ─────────────────────────────────────────────
def filter_by_user():
    print("\n── Filter by userId ─────────────────")
    r = requests.get(f"{BASE_URL}/todos", params={"userId": 1, "_limit": 3})
    for todo in r.json():
        print(f"  [id={todo['id']}] completed={todo['completed']} → {todo['title'][:45]}")


# ─────────────────────────────────────────────
# 2. Combined filtering (multiple params)
# ─────────────────────────────────────────────
def combine_filters():
    print("\n── Combined Filters ─────────────────")
    r = requests.get(f"{BASE_URL}/todos", params={"userId": 1, "completed": "false", "_limit": 3})
    open_todos = r.json()
    print(f"  Open todos for user 1: {len(open_todos)} shown")
    for todo in open_todos:
        print(f"    - {todo['title'][:50]}")


# ─────────────────────────────────────────────
# 3. Sorting locally (API may not sort)
# ─────────────────────────────────────────────
def sort_results():
    print("\n── Local Sorting ────────────────────")
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 10})
    posts = r.json()
    by_title = sorted(posts, key=lambda p: p["title"].lower())
    print("  Posts sorted by title (asc):")
    for p in by_title:
        print(f"    {p['title'][:55]}")


# ─────────────────────────────────────────────
# 4. Projection — request only needed fields
# ─────────────────────────────────────────────
def field_projection():
    print("\n── Field Projection ─────────────────")
    r = requests.get(f"{BASE_URL}/users/1")
    user = r.json()
    wanted = ["id", "name", "email"]
    print(f"  Projected user: { {k: user[k] for k in wanted} }")


if __name__ == "__main__":
    print("=" * 55)
    print("  FILTERING & SORTING: query parameters")
    print("=" * 55)
    filter_by_user()
    combine_filters()
    sort_results()
    field_projection()
    print("\nFiltering/sorting demos complete.")