"""
📘 TOPIC 36: Web Mining Workflows — APIs + Scraping
==================================================
Real-world pipelines mix REST APIs with scraping when data
isn't fully available via an API.

Typical flow:
  1. API for the structured records (metadata)
  2. Scraper for the detail pages (html/blobs)
  3. Normalize, validate, store
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Fetch records via API
# ─────────────────────────────────────────────
def fetch_via_api():
    print("\n── Step 1: API Fetch ────────────────")
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 3})
    posts = r.json()
    print(f"  Got {len(posts)} posts from the API")
    for p in posts:
        print(f"    [{p['id']}] {p['title'][:45]}")
    return posts


# ─────────────────────────────────────────────
# 2. Augment with a second resource (scrape-sim)
# ─────────────────────────────────────────────
def augment_details(posts):
    print("\n── Step 2: Augment Details ──────────")
    enriched = []
    for p in posts:
        author = requests.get(f"{BASE_URL}/users/{p['userId']}").json()
        enriched.append({
            "post_id": p["id"],
            "title": p["title"],
            "author": author["name"],
            "author_email": author["email"],
        })
        print(f"    post {p['id']} ← author {author['name']}")
    return enriched


# ─────────────────────────────────────────────
# 3. Normalize into a clean schema
# ─────────────────────────────────────────────
def normalize(enriched):
    print("\n── Step 3: Normalize ────────────────")
    for row in enriched:
        clean = {k: (v or "").strip() for k, v in row.items()}
        print(f"    {json.dumps(clean)}")


# ─────────────────────────────────────────────
# 4. Pipeline orchestration
# ─────────────────────────────────────────────
def run_pipeline():
    posts = fetch_via_api()
    enriched = augment_details(posts)
    normalize(enriched)
    print("\n  Pipeline complete → ready for storage/analysis")


if __name__ == "__main__":
    print("=" * 55)
    print("  WEB MINING: APIs + scraping pipeline")
    print("=" * 55)
    run_pipeline()
    print("\nWorkflow demos complete.")