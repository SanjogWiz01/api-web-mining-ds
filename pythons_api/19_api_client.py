"""Real implementation: a reusable, production-style API client.

Features:
  - Session reuse, timeouts, retries with backoff
  - Automatic bearer-token injection
  - Unified error handling (custom exceptions)
  - Response caching (in-memory, TTL)
  - Pagination helper

Designed to talk to any REST JSON API. Run the self-test at the bottom
against JSONPlaceholder.

Run:  python 19_api_client.py
"""

import hashlib
import json
import time
from collections import OrderedDict
from typing import Any, Iterator

import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class ApiError(Exception):
    pass


class ApiClient:
    def __init__(
        self,
        base_url: str,
        *,
        token: str = "",
        timeout: tuple[float, float] = (3.05, 15.0),
        max_retries: int = 3,
        cache_ttl: float = 60.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.cache_ttl = cache_ttl
        self._cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self._token = token

        retry = Retry(
            total=max_retries,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "HEAD", "OPTIONS"]),
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session = requests.Session()
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update({"Accept": "application/json", "User-Agent": "api-client/1.0"})
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    # ------------------------------------------------------------------ core
    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = self.base_url + path
        kwargs.setdefault("timeout", self.timeout)

        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise ApiError(f"{method} {path} failed: {exc}") from exc

        if response.status_code >= 400:
            raise self._make_error(response)

        if not response.content:
            return {}
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise ApiError("response body is not valid JSON") from exc

    def _make_error(self, response: requests.Response) -> ApiError:
        body = response.text[:300]
        return ApiError(f"HTTP {response.status_code} on {response.request.url}: {body}")

    # ------------------------------------------------------------------ verbs
    def get(self, path: str, *, use_cache: bool = True, **kwargs: Any) -> dict[str, Any]:
        cache_key = self._cache_key("GET", path, kwargs)
        if use_cache:
            hit = self._cache_get(cache_key)
            if hit is not None:
                return hit

        data = self.request("GET", path, **kwargs)
        self._cache_set(cache_key, data)
        return data

    def post(self, path: str, json: Any = None, **kwargs: Any) -> dict[str, Any]:
        return self.request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: Any = None, **kwargs: Any) -> dict[str, Any]:
        return self.request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.request("DELETE", path, **kwargs)

    # ------------------------------------------------------------------ cache
    def _cache_key(self, method: str, path: str, kwargs: Any) -> str:
        raw = json.dumps([method, path, kwargs.get("params")], sort_keys=True, default=str)
        return hashlib.md5(raw.encode()).hexdigest()

    def _cache_get(self, key: str) -> Any | None:
        entry = self._cache.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.monotonic() > expires_at:
            self._cache.pop(key, None)
            return None
        self._cache.move_to_end(key)
        return value

    def _cache_set(self, key: str, value: Any) -> None:
        self._cache[key] = (time.monotonic() + self.cache_ttl, value)
        self._cache.move_to_end(key)
        while len(self._cache) > 128:
            self._cache.popitem(last=False)

    # -------------------------------------------------------------- pagination
    def iter_pages(self, path: str, *, page_param: str = "_page",
                   size_param: str = "_limit", page_size: int = 20,
                   **kwargs: Any) -> Iterator[list[dict[str, Any]]]:
        page = 1
        while True:
            params = dict(kwargs.get("params") or {})
            params.update({page_param: page, size_param: page_size})
            result = self.get(path, params=params, use_cache=False)
            items = result if isinstance(result, list) else result.get("data", [])
            yield items
            if len(items) < page_size:
                break
            page += 1


def self_test() -> None:
    client = ApiClient("https://jsonplaceholder.typicode.com")

    print("== get one ==")
    post = client.get("/posts/1")
    print(f"  title: {post['title'][:40]}")

    print("== cache (should be instant, no network) ==")
    t0 = time.perf_counter()
    client.get("/posts/1")
    print(f"  cached in {(time.perf_counter() - t0) * 1000:.2f} ms")

    print("== create (POST) ==")
    created = client.post("/posts", json={"title": "New", "body": "x", "userId": 1})
    print(f"  created id={created.get('id')}")

    print("== pagination ==")
    total = 0
    for items in client.iter_pages("/posts", page_size=5):
        total += len(items)
        print(f"  page has {len(items)} items")
    print(f"  total collected: {total}")

    print("== 404 becomes ApiError ==")
    try:
        client.get("/posts/999999999")
    except ApiError as e:
        print(f"  {type(e).__name__}: {e}")


if __name__ == "__main__":
    self_test()
