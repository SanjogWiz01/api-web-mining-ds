from __future__ import annotations

import pytest
import requests

from api_web_mining_ds.http_client import ApiClient, ApiClientConfig, ApiError, RateLimitError


class FakeResponse:
    def __init__(self, status_code: int, payload=None, *, url: str = "https://api.test/items", headers=None):
        self.status_code = status_code
        self._payload = payload
        self.url = url
        self.headers = headers or {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, **kwargs})
        return self.responses.pop(0)


def test_get_json_retries_transient_server_errors(monkeypatch):
    monkeypatch.setattr("api_web_mining_ds.http_client.time.sleep", lambda _: None)
    session = FakeSession(
        [
            FakeResponse(503, {"error": "temporary"}),
            FakeResponse(200, {"items": [{"id": 1}]}),
        ]
    )
    client = ApiClient(ApiClientConfig(retries=1, backoff_seconds=0), session=session)

    assert client.get_json("https://api.test/items") == {"items": [{"id": 1}]}
    assert len(session.calls) == 2
    assert session.calls[0]["headers"]["User-Agent"] == "api-web-mining-ds/0.1.0"


def test_get_json_raises_rate_limit_after_retries(monkeypatch):
    monkeypatch.setattr("api_web_mining_ds.http_client.time.sleep", lambda _: None)
    session = FakeSession([FakeResponse(429, {"error": "slow down"})])
    client = ApiClient(ApiClientConfig(retries=0, backoff_seconds=0), session=session)

    with pytest.raises(RateLimitError):
        client.get_json("https://api.test/items")


def test_get_json_raises_for_invalid_json():
    class InvalidJsonResponse(FakeResponse):
        def json(self):
            raise ValueError("bad json")

    session = FakeSession([InvalidJsonResponse(200)])
    client = ApiClient(ApiClientConfig(retries=0), session=session)

    with pytest.raises(ApiError):
        client.get_json("https://api.test/items")


def test_paginate_collects_until_empty_page():
    session = FakeSession(
        [
            FakeResponse(200, {"items": [{"id": 1}, {"id": 2}]}),
            FakeResponse(200, {"items": [{"id": 3}]}),
            FakeResponse(200, {"items": []}),
        ]
    )
    client = ApiClient(ApiClientConfig(retries=0), session=session)

    items = client.paginate("https://api.test/items", extract_items=lambda payload: payload["items"])

    assert items == [{"id": 1}, {"id": 2}, {"id": 3}]
    assert [call["params"]["page"] for call in session.calls] == [1, 2, 3]
