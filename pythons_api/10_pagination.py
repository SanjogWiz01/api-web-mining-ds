"""Practice file: pagination.

APIs that return large lists paginate. Patterns covered:
  - page/limit
  - offset/limit
  - cursor/next-page (via Link header or next_url field)

Run:  python 10_pagination.py
"""

from typing import Callable, Iterator

import requests


# ---------------------------------------------------------------- fake API
def fake_api(page: int, limit: int) -> dict:
    """Simulate a paginated endpoint returning an in-memory list."""
    all_items = [{"id": i, "name": f"item-{i}"} for i in range(1, 61)]
    start = (page - 1) * limit
    chunk = all_items[start:start + limit]
    return {
        "data": chunk,
        "page": page,
        "limit": limit,
        "total": len(all_items),
        "has_next": start + len(chunk) < len(all_items),
        "next": page + 1 if start + len(chunk) < len(all_items) else None,
    }


def real_jsonplaceholder() -> Iterator[dict]:
    """Real API: /posts?_page=1&_limit=5 uses page/limit pagination."""
    page = 1
    limit = 5
    while True:
        r = requests.get("https://jsonplaceholder.typicode.com/posts",
                         params={"_page": page, "_limit": limit},
                         timeout=(3, 10))
        r.raise_for_status()
        items = r.json()
        if not items:
            break
        yield from items
        page += 1


# ------------------------------------------------------------- generators
def fetch_all_pages(fetch_page: Callable[[int], dict], limit: int = 10) -> list[dict]:
    """Generator-style loop collecting every page (page/limit pattern)."""
    collected: list[dict] = []
    page = 1
    while True:
        result = fetch_page(page, limit)
        collected.extend(result["data"])
        if not result["has_next"]:
            break
        page += 1
    return collected


if __name__ == "__main__":
    print("== fake paginated api ==")
    all_items = fetch_all_pages(fake_api, limit=10)
    print(f"  collected {len(all_items)} items (should be 60)")

    print("== real JSONPlaceholder pagination ==")
    count = 0
    for post in real_jsonplaceholder():
        count += 1
    print(f"  collected {count} posts")

    print("== manual page walk ==")
    page = 1
    while True:
        result = fake_api(page, 20)
        print(f"  page {page}: {len(result['data'])} items, next={result['next']}")
        if result["next"] is None:
            break
        page = result["next"]
