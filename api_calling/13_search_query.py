"""
📘 TOPIC 13: Search Queries — q, search, full-text
==================================================
Many APIs expose a search endpoint or a `q`/`search` parameter
that performs full-text matching server-side.

JSONPlaceholder mimics this with a `q` param on /posts.
"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Simple keyword search
# ─────────────────────────────────────────────
def simple_search():
    print("\n── Simple Keyword Search ────────────")
    r = requests.get(f"{BASE_URL}/posts", params={"q": "qui", "_limit": 5})
    results = r.json()
    print(f"  Found {len(results)} posts containing 'qui':")
    for p in results:
        print(f"    [{p['id']}] {p['title'][:55]}")


# ─────────────────────────────────────────────
# 2. Search with additional filters
# ─────────────────────────────────────────────
def search_plus_filter():
    print("\n── Search + Filter ──────────────────")
    r = requests.get(f"{BASE_URL}/comments", params={"q": "alias", "_limit": 3})
    comments = r.json()
    print(f"  Comments matching 'alias': {len(comments)}")
    for c in comments:
        print(f"    - {c['name'][:55]}")


# ─────────────────────────────────────────────
# 3. Search across multiple endpoints
# ─────────────────────────────────────────────
def multi_endpoint_search():
    print("\n── Multi-Endpoint Search ────────────")
    term = "sunt"
    for resource in ("posts", "albums"):
        r = requests.get(f"{BASE_URL}/{resource}", params={"q": term, "_limit": 2})
        data = r.json()
        print(f"  {resource}: {len(data)} matches for '{term}'")


# ─────────────────────────────────────────────
# 4. Case-insensitive local search fallback
# ─────────────────────────────────────────────
def local_search_fallback():
    print("\n── Local Search Fallback ────────────")
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 50})
    term = "ipsum"
    matches = [p for p in r.json() if term in p["title"].lower()]
    print(f"  {len(matches)} of 50 posts contain '{term}' (client-side)")


if __name__ == "__main__":
    print("=" * 55)
    print("  SEARCH QUERIES: q/search parameters")
    print("=" * 55)
    simple_search()
    search_plus_filter()
    multi_endpoint_search()
    local_search_fallback()
    print("\nSearch query demos complete.")