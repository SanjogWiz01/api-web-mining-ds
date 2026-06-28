"""Check robots.txt crawl policy before mining a website."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import pandas as pd
import requests


DEFAULT_SITE = "https://books.toscrape.com/"
DEFAULT_PATHS = ["/", "/catalogue/page-1.html", "/catalogue/category/books_1/index.html"]
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "robots_policy"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


def robots_url(site_url: str) -> str:
    parsed = urlparse(site_url)
    return f"{parsed.scheme}://{parsed.netloc}/robots.txt"


def load_robot_parser(site_url: str) -> tuple[RobotFileParser, str]:
    robot_url = robots_url(site_url)
    response = requests.get(robot_url, headers=HEADERS, timeout=15)

    parser = RobotFileParser()
    parser.set_url(robot_url)
    if response.status_code == 404:
        parser.parse([])
    else:
        response.raise_for_status()
        parser.parse(response.text.splitlines())
    return parser, robot_url


def check_paths(site_url: str = DEFAULT_SITE, paths: list[str] | None = None) -> pd.DataFrame:
    parser, robot_url = load_robot_parser(site_url)
    checked_paths = paths or DEFAULT_PATHS

    rows: list[dict[str, object]] = []
    for path in checked_paths:
        target_url = urljoin(site_url, path)
        rows.append(
            {
                "robots_url": robot_url,
                "target_url": target_url,
                "user_agent": HEADERS["User-Agent"],
                "allowed": parser.can_fetch(HEADERS["User-Agent"], target_url),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    policy = check_paths()

    csv_path = OUTPUT_DIR / "robots_policy_check.csv"
    policy.to_csv(csv_path, index=False)

    allowed = int(policy["allowed"].sum())
    print(f"Checked {len(policy)} paths; {allowed} allowed")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
