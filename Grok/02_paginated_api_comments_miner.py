"""Collect paginated API records and create a compact comment dataset.

Source: https://jsonplaceholder.typicode.com/comments
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import requests


BASE_URL = "https://jsonplaceholder.typicode.com/comments"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "paginated_comments"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


def fetch_comment_page(start: int, limit: int) -> list[dict[str, Any]]:
    response = requests.get(
        BASE_URL,
        params={"_start": start, "_limit": limit},
        headers=HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        raise TypeError("Expected a list of comments")
    return payload


def collect_comments(limit: int = 50, max_pages: int = 4) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for page in range(max_pages):
        start = page * limit
        comments = fetch_comment_page(start=start, limit=limit)
        if not comments:
            break
        rows.extend(comments)

    comments_df = pd.DataFrame(rows)
    if comments_df.empty:
        return comments_df

    comments_df["email_domain"] = comments_df["email"].str.split("@").str[-1].str.lower()
    comments_df["comment_word_count"] = comments_df["body"].str.split().str.len()
    comments_df["body_preview"] = comments_df["body"].str.replace(r"\s+", " ", regex=True).str[:80]
    return comments_df.sort_values(["postId", "id"]).reset_index(drop=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    comments = collect_comments()

    csv_path = OUTPUT_DIR / "comments_sample.csv"
    summary_path = OUTPUT_DIR / "comments_by_post.csv"

    comments.to_csv(csv_path, index=False)
    summary = (
        comments.groupby("postId", as_index=False)
        .agg(comments=("id", "count"), avg_words=("comment_word_count", "mean"))
        .round({"avg_words": 2})
    )
    summary.to_csv(summary_path, index=False)

    print(f"Mined {len(comments)} comments")
    print(f"Rows: {csv_path}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    main()
