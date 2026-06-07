from __future__ import annotations

import asyncio
from pathlib import Path
import sys

import pandas as pd

from api_web_mining_ds.async_client import AsyncApiConfig, fetch_json_many
from api_web_mining_ds.profiling import profile_dataframe
from api_web_mining_ds.text_mining import keyword_counts, tokenize, top_terms


def test_profile_dataframe_reports_missing_and_unique_counts():
    df = pd.DataFrame({"name": ["Ada", "Grace", None], "score": [10, 10, 20]})

    profile = profile_dataframe(df).set_index("column")

    assert profile.loc["name", "missing"] == 1
    assert profile.loc["score", "unique"] == 2


def test_text_mining_helpers_count_terms_and_keywords():
    texts = ["API mining with Python", "Python API data project"]

    assert tokenize("The API is useful") == ["api", "useful"]
    assert top_terms(texts, n=2)["term"].tolist() == ["api", "python"]
    assert keyword_counts(texts, ["api", "python"])["api"].tolist() == [1, 1]


def test_fetch_json_many_uses_async_httpx_client(monkeypatch):
    class FakeAsyncResponse:
        def __init__(self, url):
            self.url = url

        def raise_for_status(self):
            return None

        def json(self):
            return {"url": self.url}

    class FakeAsyncClient:
        def __init__(self, timeout, headers):
            self.timeout = timeout
            self.headers = headers

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, traceback):
            return None

        async def get(self, url):
            return FakeAsyncResponse(url)

    monkeypatch.setattr("api_web_mining_ds.async_client.httpx.AsyncClient", FakeAsyncClient)

    results = asyncio.run(
        fetch_json_many(
            ["https://api.test/a", "https://api.test/b"],
            config=AsyncApiConfig(concurrency=1, timeout=3),
        )
    )

    assert results == [{"url": "https://api.test/a"}, {"url": "https://api.test/b"}]


def test_cli_smoke_runs_with_mocked_pipeline(monkeypatch, capsys):
    from api_web_mining_ds import cli

    class Outputs:
        raw_json = Path("raw.json")
        clean_csv = Path("clean.csv")
        sqlite_db = Path("data.sqlite")
        profile_csv = Path("profile.csv")
        terms_csv = Path("terms.csv")

    monkeypatch.setattr(sys, "argv", ["api-web-mine", "jsonplaceholder-posts", "--output-dir", "tmp"])
    monkeypatch.setattr(cli, "collect_posts_project", lambda client, output_dir: Outputs())

    cli.main()

    assert "Clean CSV: clean.csv" in capsys.readouterr().out
