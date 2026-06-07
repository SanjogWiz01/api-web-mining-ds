# Advanced API & Web Mining for Data Science

Practical Python course material for collecting, cleaning, storing, and analyzing web data from APIs and HTML pages. The repo is organized like a real data project: reusable source code, runnable examples, tests, and course documentation.

## What You Will Build

- API clients with timeouts, retries, headers, pagination, and rate-limit handling.
- JSON-to-DataFrame pipelines for nested API responses.
- Web mining utilities for static HTML, tables, links, pagination, and polite scraping.
- Async collection workflows with `httpx`.
- Storage helpers for JSON, CSV, and SQLite.
- Text mining and dataset profiling utilities for practical analysis.
- End-to-end mini projects that collect, clean, store, analyze, and report on web data.

## Repository Layout

```text
api-web-mining-ds/
├── docs/                       # Course lessons and project notes
├── examples/                   # Runnable practical examples
├── src/api_web_mining_ds/      # Reusable Python package
├── tests/                      # Mocked tests; no live web dependency
├── node-app/                   # Optional Node package manifests only
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Quick Start on Windows

```powershell
cd C:\Users\sanjo\OneDrive\Attachments\Desktop\Assembly\api-web-mining-ds
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
```

## Run Practical Examples

```powershell
python examples\01_fetch_jsonplaceholder.py
python examples\02_weather_open_meteo.py
python examples\03_scrape_static_html.py
python examples\04_end_to_end_pipeline.py
```

Examples that call live websites are designed for learning. Tests use mocked responses so the project remains stable offline and in CI.

## Course Path

1. Read `docs/01_api_fundamentals.md` for requests, status codes, auth, pagination, and rate limits.
2. Read `docs/02_web_mining_workflow.md` for scraping ethics, robots.txt, selectors, and table extraction.
3. Read `docs/03_data_pipeline_project.md` and run the end-to-end pipeline example.
4. Use `docs/04_expansion_roadmap.md` to expand this v1 course into a larger book-sized curriculum without adding filler.

## Ethical Use

Only collect data from sources you are allowed to access. Respect website terms, robots.txt, authentication boundaries, rate limits, copyright, and privacy. This repo teaches polite collection patterns and uses public/demo endpoints for examples.

## Development

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

The test suite covers API retry behavior, pagination, JSON normalization, scraping extraction, storage, profiling, and text mining with deterministic fixtures.

## Pull Request Scope

This is a realistic v1 implementation, not a fake 500-page dump. It provides a working professional base and a clear roadmap for turning it into a full long-form course over staged PRs.
