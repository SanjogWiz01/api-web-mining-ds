"""
📘 TOPIC 39: Storing API Data — Databases & Files
================================================
Once you mine data from APIs, you need to store it:
CSV/JSON for small datasets, SQLite for structured queries.

This demo writes clean API data to JSON and CSV.
"""

import requests
import json
import csv
import os

BASE_URL = "https://jsonplaceholder.typicode.com"


def fetch_posts():
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 10})
    r.raise_for_status()
    return r.json()


def save_json(posts, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)
    print(f"  JSON → {path} ({len(posts)} records)")


def save_csv(posts, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "userId", "title", "body"])
        writer.writeheader()
        writer.writerows(posts)
    print(f"  CSV  → {path} ({len(posts)} records)")


def demo_store():
    print("\n── Store API Data ───────────────────")
    posts = fetch_posts()
    print(f"  Fetched {len(posts)} posts from API")
    save_json(posts, "posts_export.json")
    save_csv(posts, "posts_export.csv")


def cleanup():
    print("\n── Cleanup Demo Files ──────────────")
    for f in ("posts_export.json", "posts_export.csv"):
        if os.path.exists(f):
            os.remove(f)
            print(f"  Removed {f}")


def storage_options():
    print("\n── Storage Options ──────────────────")
    options = [
        ("JSON/CSV", "Small data, human-readable, easy to share"),
        ("SQLite", "Structured queries, joins, no server needed"),
        ("Postgres/MySQL", "Multi-user, production, scaling"),
        ("Data warehouse", "Analytics at scale (BigQuery, Redshift)"),
    ]
    for name, desc in options:
        print(f"  {name:<12} {desc}")


if __name__ == "__main__":
    print("=" * 55)
    print("  STORING API DATA: json/csv/sql")
    print("=" * 55)
    demo_store()
    storage_options()
    cleanup()
    print("\nStorage demos complete.")