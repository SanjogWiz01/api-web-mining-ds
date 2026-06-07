from api_web_mining_ds.scraper import HtmlScraper, RobotsPolicy, build_next_page_urls


HTML = """
<html>
  <body>
    <a href="/a">A link</a>
    <article class="card">
      <h2>First item</h2>
      <span class="price">$10</span>
    </article>
    <article class="card">
      <h2>Second item</h2>
      <span class="price">$20</span>
    </article>
    <table>
      <tr><th>Name</th><th>Score</th></tr>
      <tr><td>Ada</td><td>10</td></tr>
    </table>
  </body>
</html>
"""


class FakeHtmlResponse:
    status_code = 200
    text = HTML

    def raise_for_status(self):
        return None


class FakeHtmlSession:
    def __init__(self):
        self.calls = []

    def get(self, url, **kwargs):
        self.calls.append({"url": url, **kwargs})
        return FakeHtmlResponse()


def test_extract_links_resolves_relative_urls():
    scraper = HtmlScraper()

    links = scraper.extract_links(HTML, base_url="https://example.com/root/")

    assert links == [{"text": "A link", "url": "https://example.com/a"}]


def test_extract_cards_maps_css_selectors():
    scraper = HtmlScraper()

    cards = scraper.extract_cards(HTML, card_selector=".card", fields={"name": "h2", "price": ".price"})

    assert cards == [{"name": "First item", "price": "$10"}, {"name": "Second item", "price": "$20"}]


def test_extract_tables_returns_dataframes():
    scraper = HtmlScraper()

    tables = scraper.extract_tables(HTML)

    assert tables[0].loc[0, "Name"] == "Ada"
    assert tables[0].loc[0, "Score"] == 10


def test_fetch_soup_can_skip_robots_for_local_tests():
    session = FakeHtmlSession()
    scraper = HtmlScraper(robots_policy=RobotsPolicy(respect_robots_txt=False), session=session)

    soup = scraper.fetch_soup("https://example.com/page")

    assert soup.select_one("h2").get_text(strip=True) == "First item"
    assert session.calls[0]["headers"]["User-Agent"] == "api-web-mining-ds/0.1.0"


def test_build_next_page_urls_adds_query_params():
    assert build_next_page_urls("https://example.com/search?q=api", start=2, stop=3) == [
        "https://example.com/search?q=api&page=2",
        "https://example.com/search?q=api&page=3",
    ]
