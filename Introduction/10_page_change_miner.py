"""Track page content hashes to detect changes between mining runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup
import pandas as pd
import requests


URLS = [
    "https://example.com/",
    "https://books.toscrape.com/",
    "https://quotes.toscrape.com/",
]
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "page_changes"
STATE_PATH = OUTPUT_DIR / "page_hash_state.json"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


@dataclass(frozen=True)
class PageSnapshot:
    url: str
    status_code: int
    title: str
    text_hash: str
    text_length: int
    checked_at: str


def load_state() -> dict[str, dict[str, object]]:
    if not STATE_PATH.exists():
        return {}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(snapshots: list[PageSnapshot]) -> None:
    STATE_PATH.write_text(
        json.dumps({snapshot.url: asdict(snapshot) for snapshot in snapshots}, indent=2),
        encoding="utf-8",
    )


def fetch_snapshot(url: str) -> PageSnapshot:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    text = soup.get_text(" ", strip=True)
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

    return PageSnapshot(
        url=url,
        status_code=response.status_code,
        title=title,
        text_hash=text_hash,
        text_length=len(text),
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def detect_changes(urls: list[str] | None = None) -> pd.DataFrame:
    previous_state = load_state()
    snapshots = [fetch_snapshot(url) for url in (urls or URLS)]

    rows: list[dict[str, object]] = []
    for snapshot in snapshots:
        previous = previous_state.get(snapshot.url, {})
        previous_hash = previous.get("text_hash")
        rows.append(
            {
                **asdict(snapshot),
                "previous_hash": previous_hash or "",
                "changed": bool(previous_hash and previous_hash != snapshot.text_hash),
                "first_seen": previous_hash is None,
            }
        )

    save_state(snapshots)
    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    changes = detect_changes()

    csv_path = OUTPUT_DIR / "page_change_report.csv"
    changes.to_csv(csv_path, index=False)

    changed_count = int(changes["changed"].sum())
    print(f"Checked {len(changes)} pages; {changed_count} changed since last run")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
