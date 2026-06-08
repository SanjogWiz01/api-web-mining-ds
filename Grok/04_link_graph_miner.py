"""Extract same-site and external links from a static HTML page."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
import pandas as pd
import requests


DEFAULT_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "link_graph"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}


def normalize_url(base_url: str, href: str) -> str | None:
    if not href or href.startswith(("mailto:", "tel:", "javascript:")):
        return None
    absolute = urljoin(base_url, href)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    return absolute.split("#", 1)[0]


def mine_links(url: str = DEFAULT_URL) -> pd.DataFrame:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    source_domain = urlparse(url).netloc
    rows: list[dict[str, str]] = []

    for anchor in soup.select("a[href]"):
        target_url = normalize_url(url, anchor.get("href", ""))
        if target_url is None:
            continue

        target_domain = urlparse(target_url).netloc
        rows.append(
            {
                "source_url": url,
                "anchor_text": anchor.get_text(" ", strip=True),
                "target_url": target_url,
                "target_domain": target_domain,
                "link_type": "internal" if target_domain == source_domain else "external",
            }
        )

    return pd.DataFrame(rows).drop_duplicates(subset=["source_url", "target_url"])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    links = mine_links()

    csv_path = OUTPUT_DIR / "links.csv"
    domain_path = OUTPUT_DIR / "target_domains.csv"

    links.to_csv(csv_path, index=False)
    domain_counts = Counter(links["target_domain"])
    pd.DataFrame(domain_counts.items(), columns=["target_domain", "links"]).to_csv(domain_path, index=False)

    print(f"Mined {len(links)} unique links")
    print(f"Links: {csv_path}")
    print(f"Domains: {domain_path}")


if __name__ == "__main__":
    main()
