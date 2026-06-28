"""Mine top Hacker News story metadata with concurrent HTTP requests."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import httpx
import pandas as pd


BASE_URL = "https://hacker-news.firebaseio.com/v0"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "hackernews_async"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


async def fetch_json(client: httpx.AsyncClient, path: str) -> Any:
    response = await client.get(f"{BASE_URL}/{path}", timeout=15)
    response.raise_for_status()
    return response.json()


async def fetch_story(client: httpx.AsyncClient, story_id: int) -> dict[str, Any]:
    item = await fetch_json(client, f"item/{story_id}.json")
    if not isinstance(item, dict):
        return {"id": story_id, "missing": True}
    return item


async def collect_top_stories(limit: int = 30) -> pd.DataFrame:
    async with httpx.AsyncClient(headers=HEADERS) as client:
        story_ids = await fetch_json(client, "topstories.json")
        selected_ids = list(story_ids[:limit])
        stories = await asyncio.gather(*(fetch_story(client, story_id) for story_id in selected_ids))

    frame = pd.DataFrame(stories)
    keep_columns = ["id", "title", "by", "score", "descendants", "time", "url"]
    for column in keep_columns:
        if column not in frame.columns:
            frame[column] = None

    frame = frame[keep_columns].rename(columns={"by": "author", "descendants": "comments"})
    frame["rank"] = range(1, len(frame) + 1)
    frame["source"] = "hacker-news-firebase-api"
    return frame


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stories = asyncio.run(collect_top_stories())

    csv_path = OUTPUT_DIR / "top_stories.csv"
    stories.to_csv(csv_path, index=False)

    print(f"Mined {len(stories)} top stories")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
