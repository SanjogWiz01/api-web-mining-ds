"""Scrape product cards from the Books to Scrape demo catalog.

Source: https://books.toscrape.com/
"""

from __future__ import annotations

from pathlib import Path
from time import sleep
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import pandas as pd
import requests


BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "books_catalog"
HEADERS = {"User-Agent": "api-web-mining-ds-learning/1.0"}
RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def fetch_soup(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    return BeautifulSoup(response.text, "lxml")


def parse_book_cards(soup: BeautifulSoup, page_url: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for card in soup.select("article.product_pod"):
        title_link = card.select_one("h3 a")
        price = card.select_one(".price_color")
        availability = card.select_one(".availability")
        rating = card.select_one("p.star-rating")

        rating_name = next((name for name in RATING_MAP if rating and name in rating.get("class", [])), None)
        relative_url = title_link.get("href", "") if title_link else ""

        rows.append(
            {
                "title": title_link.get("title", "").strip() if title_link else "",
                "price": price.get_text(strip=True) if price else "",
                "availability": availability.get_text(" ", strip=True) if availability else "",
                "rating": RATING_MAP.get(rating_name, 0),
                "book_url": urljoin(page_url, relative_url),
                "page_url": page_url,
            }
        )

    return rows


def next_page_url(soup: BeautifulSoup, page_url: str) -> str | None:
    next_link = soup.select_one("li.next a")
    if next_link is None:
        return None
    return urljoin(page_url, next_link.get("href", ""))


def scrape_catalog(max_pages: int = 3, delay_seconds: float = 0.5) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    page_url: str | None = BASE_URL

    for _ in range(max_pages):
        if page_url is None:
            break
        soup = fetch_soup(page_url)
        rows.extend(parse_book_cards(soup, page_url))
        page_url = next_page_url(soup, page_url)
        sleep(delay_seconds)

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    books = scrape_catalog()

    csv_path = OUTPUT_DIR / "books_catalog_sample.csv"
    books.to_csv(csv_path, index=False)

    print(f"Scraped {len(books)} books")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
