"""Scrape demo quotes and mine simple term frequencies.

Source: https://quotes.toscrape.com/
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import pandas as pd
import requests


BASE_URL = "https://quotes.toscrape.com/"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "quotes_text"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


def fetch_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def parse_quotes(soup: BeautifulSoup, page_url: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for quote in soup.select(".quote"):
        text = quote.select_one(".text")
        author = quote.select_one(".author")
        tags = [tag.get_text(strip=True) for tag in quote.select(".tags .tag")]
        rows.append(
            {
                "quote": text.get_text(" ", strip=True) if text else "",
                "author": author.get_text(strip=True) if author else "",
                "tags": ", ".join(tags),
                "page_url": page_url,
            }
        )
    return rows


def next_page_url(soup: BeautifulSoup, page_url: str) -> str | None:
    next_link = soup.select_one("li.next a")
    if next_link is None:
        return None
    return urljoin(page_url, next_link.get("href", ""))


def collect_quotes(max_pages: int = 3, delay_seconds: float = 0.5) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    page_url: str | None = BASE_URL

    for _ in range(max_pages):
        if page_url is None:
            break
        soup = fetch_soup(page_url)
        rows.extend(parse_quotes(soup, page_url))
        page_url = next_page_url(soup, page_url)
        sleep(delay_seconds)

    return pd.DataFrame(rows)


def mine_terms(quotes: pd.DataFrame, top_n: int = 25) -> pd.DataFrame:
    terms: Counter[str] = Counter()
    for quote in quotes["quote"].dropna():
        words = re.findall(r"[a-zA-Z]{3,}", quote.lower())
        terms.update(word for word in words if word not in STOPWORDS)
    return pd.DataFrame(terms.most_common(top_n), columns=["term", "frequency"])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    quotes = collect_quotes()
    terms = mine_terms(quotes)

    quotes_path = OUTPUT_DIR / "quotes.csv"
    terms_path = OUTPUT_DIR / "top_terms.csv"

    quotes.to_csv(quotes_path, index=False)
    terms.to_csv(terms_path, index=False)

    print(f"Mined {len(quotes)} quotes")
    print(f"Quotes: {quotes_path}")
    print(f"Terms: {terms_path}")


if __name__ == "__main__":
    main()
