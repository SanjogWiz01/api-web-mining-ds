"""HTML scraping helpers focused on polite, inspectable extraction."""

from __future__ import annotations

from dataclasses import dataclass
from io import StringIO
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

from bs4 import BeautifulSoup
import pandas as pd
import requests


@dataclass(frozen=True)
class RobotsPolicy:
    respect_robots_txt: bool = True
    user_agent: str = "api-web-mining-ds/0.1.0"


class HtmlScraper:
    """Fetch and parse static HTML pages."""

    def __init__(
        self,
        *,
        user_agent: str = "api-web-mining-ds/0.1.0",
        timeout: float = 10.0,
        robots_policy: RobotsPolicy | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.user_agent = user_agent
        self.timeout = timeout
        self.robots_policy = robots_policy or RobotsPolicy(user_agent=user_agent)
        self.session = session or requests.Session()
        self._robots_cache: dict[str, RobotFileParser] = {}

    def fetch_soup(self, url: str) -> BeautifulSoup:
        if not self.can_fetch(url):
            raise PermissionError(f"robots.txt disallows fetching {url}")

        response = self.session.get(url, headers={"User-Agent": self.user_agent}, timeout=self.timeout)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def extract_links(self, html: str, *, base_url: str | None = None, selector: str = "a") -> list[dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        links: list[dict[str, str]] = []
        for anchor in soup.select(selector):
            href = anchor.get("href")
            if not href:
                continue
            links.append(
                {
                    "text": " ".join(anchor.get_text(" ", strip=True).split()),
                    "url": urljoin(base_url, href) if base_url else href,
                }
            )
        return links

    def extract_cards(self, html: str, *, card_selector: str, fields: dict[str, str]) -> list[dict[str, str | None]]:
        soup = BeautifulSoup(html, "html.parser")
        rows: list[dict[str, str | None]] = []
        for card in soup.select(card_selector):
            row: dict[str, str | None] = {}
            for output_name, selector in fields.items():
                element = card.select_one(selector)
                row[output_name] = " ".join(element.get_text(" ", strip=True).split()) if element else None
            rows.append(row)
        return rows

    def extract_tables(self, html: str) -> list[pd.DataFrame]:
        return pd.read_html(StringIO(html))

    def can_fetch(self, url: str) -> bool:
        if not self.robots_policy.respect_robots_txt:
            return True

        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return True

        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        parser = self._robots_cache.get(robots_url)
        if parser is None:
            parser = RobotFileParser()
            parser.set_url(robots_url)
            try:
                parser.read()
            except Exception:
                return True
            self._robots_cache[robots_url] = parser

        return parser.can_fetch(self.robots_policy.user_agent, url)


def build_next_page_urls(base_url: str, *, page_param: str = "page", start: int = 1, stop: int = 5) -> list[str]:
    """Create simple query-param pagination URLs for examples."""

    separator = "&" if "?" in base_url else "?"
    return [f"{base_url}{separator}{page_param}={page}" for page in range(start, stop + 1)]
