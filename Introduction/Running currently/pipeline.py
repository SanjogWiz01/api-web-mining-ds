"""End-to-end project helpers used by examples and tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from .http_client import ApiClient
from .normalize import normalize_json, select_fields
from .profiling import profile_dataframe
from .storage import save_csv, save_json, save_sqlite
from .text_mining import top_terms


@dataclass(frozen=True)
class PipelineOutputs:
    raw_json: Path
    clean_csv: Path
    sqlite_db: Path
    profile_csv: Path
    terms_csv: Path


def collect_posts_project(
    *,
    client: ApiClient,
    output_dir: str | Path = "data/jsonplaceholder_posts",
) -> PipelineOutputs:
    """Collect JSONPlaceholder posts, clean them, store them, and create reports."""

    output_path = Path(output_dir)
    payload: Any = client.get_json("https://jsonplaceholder.typicode.com/posts")
    raw_path = save_json(payload, output_path / "raw_posts.json")

    df = normalize_json(payload)
    df = df.rename(columns={"userId": "user_id"})
    clean_df = df[["user_id", "id", "title", "body"]].dropna().copy()
    clean_df["title_length"] = clean_df["title"].str.len()
    clean_df["body_word_count"] = clean_df["body"].str.split().str.len()

    clean_path = save_csv(clean_df, output_path / "clean_posts.csv")
    db_path = save_sqlite(clean_df, output_path / "posts.sqlite", table_name="posts")

    profile = profile_dataframe(clean_df)
    profile_path = save_csv(profile, output_path / "profile.csv")

    terms = top_terms(clean_df["title"], n=15)
    terms_path = save_csv(terms, output_path / "top_title_terms.csv")

    return PipelineOutputs(
        raw_json=raw_path,
        clean_csv=clean_path,
        sqlite_db=db_path,
        profile_csv=profile_path,
        terms_csv=terms_path,
    )


def clean_news_articles(articles: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert News API-style article records into a clean DataFrame."""

    rows = select_fields(
        articles,
        {
            "title": "title",
            "author": "author",
            "source": "source.name",
            "published_at": "publishedAt",
            "url": "url",
        },
    )
    df = pd.DataFrame(rows)
    return df.dropna(subset=["title", "source", "url"]).reset_index(drop=True)
