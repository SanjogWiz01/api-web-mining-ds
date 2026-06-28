"""Small CLI entrypoint for course smoke tests and local demos."""

from __future__ import annotations

import argparse
from pathlib import Path

from .http_client import ApiClient, ApiClientConfig
from .pipeline import collect_posts_project


def main() -> None:
    parser = argparse.ArgumentParser(description="Run API and web mining course examples.")
    parser.add_argument(
        "command",
        choices=["jsonplaceholder-posts"],
        help="Example pipeline to run.",
    )
    parser.add_argument("--output-dir", default="data/jsonplaceholder_posts", help="Directory for generated data.")
    args = parser.parse_args()

    client = ApiClient(ApiClientConfig(retries=2, backoff_seconds=0.2))
    if args.command == "jsonplaceholder-posts":
        outputs = collect_posts_project(client=client, output_dir=Path(args.output_dir))
        print(f"Raw JSON: {outputs.raw_json}")
        print(f"Clean CSV: {outputs.clean_csv}")
        print(f"SQLite DB: {outputs.sqlite_db}")
        print(f"Profile: {outputs.profile_csv}")
        print(f"Top terms: {outputs.terms_csv}")
