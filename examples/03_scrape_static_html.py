"""Mine links, cards, and tables from static HTML."""

from api_web_mining_ds import HtmlScraper


HTML = """
<html>
  <body>
    <a href="/products/a">Product A</a>
    <a href="/products/b">Product B</a>
    <section class="product">
      <h2>Starter API Plan</h2>
      <span class="price">$19</span>
      <p class="summary">Good for learning projects.</p>
    </section>
    <section class="product">
      <h2>Research API Plan</h2>
      <span class="price">$99</span>
      <p class="summary">Built for scheduled web mining.</p>
    </section>
    <table>
      <tr><th>Plan</th><th>Requests</th></tr>
      <tr><td>Starter</td><td>10000</td></tr>
      <tr><td>Research</td><td>100000</td></tr>
    </table>
  </body>
</html>
"""


def main() -> None:
    scraper = HtmlScraper()

    links = scraper.extract_links(HTML, base_url="https://example.com")
    cards = scraper.extract_cards(
        HTML,
        card_selector=".product",
        fields={"name": "h2", "price": ".price", "summary": ".summary"},
    )
    tables = scraper.extract_tables(HTML)

    print("Links:", links)
    print("Cards:", cards)
    print("First table:")
    print(tables[0])


if __name__ == "__main__":
    main()
