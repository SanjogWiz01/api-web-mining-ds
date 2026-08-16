"""
📘 TOPIC 11: Pagination — Page, Limit & Cursor
==============================================
APIs never return every record in one response. Instead they paginate.

Common strategies:
  page/limit  → ?page=2&limit=10   (offset-based, simple)
  cursor      → ?cursor=abc123     (keyset-based, stable for live data)
  _limit      → JSONPlaceholder style

Always check `Link` headers and response metadata (total, has_more).
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Offset-based pagination (page & limit)
# ─────────────────────────────────────────────
def paginate_with_page_limit():
    print("\n── Page/Limit Pagination ────────────")
    page, limit = 1, 5
    while True:
        r = requests.get(f"{BASE_URL}/posts", params={"page": page, "_limit": limit})
        posts = r.json()
        if not posts:
            break
        print(f"  Page {page}: {len(posts)} posts")
        for p in posts:
            print(f"    [{p['id']}] {p['title'][:50]}")
        page += 1
        if page > 3:  # demo limit
            break


# ─────────────────────────────────────────────
# 2. Cursor pagination concept
# ─────────────────────────────────────────────
def cursor_pagination():
    print("\n── Cursor Pagination ────────────────")
    cursor = None
    fetched = 0
    for _ in range(3):
        params = {"_limit": 5}
        if cursor:
            params["_start"] = cursor
        r = requests.get(f"{BASE_URL}/posts", params=params)
        posts = r.json()
        if not posts:
            break
        fetched += len(posts)
        cursor = posts[-1]["id"] + 1
        print(f"  Cursor @ {cursor}: got {len(posts)} more")
    print(f"  Total fetched: {fetched}")


# ─────────────────────────────────────────────
# 3. Read pagination metadata if provided
# ─────────────────────────────────────────────
def read_metadata():
    print("\n── Pagination Metadata ──────────────")
    r = requests.get(f"{BASE_URL}/comments", params={"_limit": 3})
    print(f"  X-Total-Count header : {r.headers.get('X-Total-Count', 'n/a')}")
    print(f"  Link header           : {r.headers.get('Link', 'n/a')}")
    print(f"  Returned              : {len(r.json())} records")


if __name__ == "__main__":
    print("=" * 55)
    print("  PAGINATION: page/limit + cursor patterns")
    print("=" * 55)
    paginate_with_page_limit()
    cursor_pagination()
    read_metadata()
    print("\nPagination demos complete.")