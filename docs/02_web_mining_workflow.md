# Web Mining Workflow

Web mining means extracting useful information from web pages. HTML is less stable than an API, so the workflow must be more careful and more inspectable.

## Before Scraping

- Check if an official API exists.
- Read the website terms and robots.txt.
- Avoid private, authenticated, copyrighted, or personal data unless you have permission.
- Start with a small number of pages.
- Use polite delays and a meaningful user agent.

## Static HTML First

Start with static pages that return useful HTML from a normal request. Inspect the page source and identify stable CSS selectors for the data you need.

```python
cards = scraper.extract_cards(
    html,
    card_selector=".product",
    fields={"name": "h2", "price": ".price"},
)
```

Avoid selectors tied to random generated class names. Prefer semantic tags, table headers, stable IDs, and structured data when available.

## Links and Pagination

Many crawls begin with a listing page and follow links to detail pages. Store discovered URLs separately from extracted records. This gives you a queue that can be retried and audited.

Pagination patterns include:

- Query parameters such as `?page=2`
- Offset parameters such as `?offset=100`
- Next buttons
- Infinite scroll APIs hidden behind browser network calls

For this v1 course, examples focus on static HTML and simple query-parameter pagination. Browser automation is intentionally outside the first implementation because it adds operational complexity.

## Tables

HTML tables are common in public datasets. `HtmlScraper.extract_tables()` wraps `pandas.read_html()` and returns a list of DataFrames. Always inspect column names and units before analysis.

## Failure Modes

- HTML structure changes.
- The site blocks unknown clients.
- Data is loaded by JavaScript after the first HTML response.
- The page returns localized or personalized content.
- Duplicate pages appear through multiple URLs.

Good scraping code makes these problems visible instead of silently producing bad data.
