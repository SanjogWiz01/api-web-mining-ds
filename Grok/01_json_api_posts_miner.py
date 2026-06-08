"""Mine posts and users from a JSON API into analysis-ready CSV files.

Source: https://jsonplaceholder.typicode.com/
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "json_api_posts"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


def fetch_json(path: str) -> list[dict[str, Any]]:
    """Fetch one JSON API collection."""

    url = f"{BASE_URL}/{path.lstrip('/')}"
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        raise TypeError(f"Expected a list from {url}")
    return payload


def mine_posts() -> pd.DataFrame:
    posts = pd.DataFrame(fetch_json("posts"))
    users = pd.DataFrame(fetch_json("users"))

    users = users.rename(columns={"id": "userId", "name": "author_name", "email": "author_email"})
    user_columns = ["userId", "author_name", "author_email", "username", "website"]

    mined = posts.merge(users[user_columns], on="userId", how="left")
    mined["title_word_count"] = mined["title"].str.split().str.len()
    mined["body_word_count"] = mined["body"].str.split().str.len()
    mined["source"] = BASE_URL
    return mined.sort_values(["userId", "id"]).reset_index(drop=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    posts = mine_posts()

    csv_path = OUTPUT_DIR / "posts_with_authors.csv"
    json_path = OUTPUT_DIR / "posts_with_authors.json"

    posts.to_csv(csv_path, index=False)
    posts.to_json(json_path, orient="records", indent=2)

    print(f"Mined {len(posts)} posts")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")


if __name__ == "__main__":
    main()
