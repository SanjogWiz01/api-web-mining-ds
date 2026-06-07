"""HTTP client helpers for practical API mining."""

from __future__ import annotations

from dataclasses import dataclass, field
import time
from typing import Any, Callable, Iterable

import requests


class ApiError(RuntimeError):
    """Raised when an API request fails after retry handling."""


class RateLimitError(ApiError):
    """Raised when a rate-limited request cannot be recovered."""


@dataclass(frozen=True)
class ApiClientConfig:
    base_url: str = ""
    timeout: float = 10.0
    retries: int = 2
    backoff_seconds: float = 0.5
    user_agent: str = "api-web-mining-ds/0.1.0"
    default_headers: dict[str, str] = field(default_factory=dict)
    rate_limit_statuses: tuple[int, ...] = (429,)
    retry_statuses: tuple[int, ...] = (500, 502, 503, 504)


class ApiClient:
    """Small requests-based client with retries, JSON parsing, and pagination."""

    def __init__(self, config: ApiClientConfig | None = None, session: requests.Session | None = None) -> None:
        self.config = config or ApiClientConfig()
        self.session = session or requests.Session()

    def get_json(
        self,
        path_or_url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        response = self._request("GET", path_or_url, params=params, headers=headers)
        try:
            return response.json()
        except ValueError as exc:
            raise ApiError(f"Response from {response.url} was not valid JSON") from exc

    def paginate(
        self,
        path_or_url: str,
        *,
        page_param: str = "page",
        start_page: int = 1,
        max_pages: int | None = None,
        params: dict[str, Any] | None = None,
        extract_items: Callable[[Any], Iterable[Any]] | None = None,
        stop_when_empty: bool = True,
    ) -> list[Any]:
        """Collect paginated JSON responses into one list."""

        collected: list[Any] = []
        page = start_page
        pages_read = 0

        while max_pages is None or pages_read < max_pages:
            page_params = dict(params or {})
            page_params[page_param] = page
            payload = self.get_json(path_or_url, params=page_params)

            if extract_items is None:
                items = payload if isinstance(payload, list) else payload.get("items", [])
            else:
                items = list(extract_items(payload))

            if stop_when_empty and not items:
                break

            collected.extend(items)
            page += 1
            pages_read += 1

        return collected

    def _request(
        self,
        method: str,
        path_or_url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        url = self._build_url(path_or_url)
        request_headers = self._headers(headers)
        last_error: Exception | None = None

        for attempt in range(self.config.retries + 1):
            try:
                response = self.session.request(
                    method,
                    url,
                    params=params,
                    headers=request_headers,
                    timeout=self.config.timeout,
                )
            except requests.RequestException as exc:
                last_error = exc
                if attempt == self.config.retries:
                    raise ApiError(f"{method} {url} failed: {exc}") from exc
                self._sleep(attempt)
                continue

            if response.status_code in self.config.rate_limit_statuses:
                if attempt == self.config.retries:
                    raise RateLimitError(f"{method} {response.url} was rate limited")
                self._sleep(attempt, response=response)
                continue

            if response.status_code in self.config.retry_statuses:
                if attempt == self.config.retries:
                    raise ApiError(f"{method} {response.url} failed with HTTP {response.status_code}")
                self._sleep(attempt)
                continue

            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                raise ApiError(f"{method} {response.url} failed with HTTP {response.status_code}") from exc

            return response

        raise ApiError(f"{method} {url} failed: {last_error}")

    def _build_url(self, path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://")):
            return path_or_url
        return f"{self.config.base_url.rstrip('/')}/{path_or_url.lstrip('/')}"

    def _headers(self, extra: dict[str, str] | None) -> dict[str, str]:
        headers = {"User-Agent": self.config.user_agent}
        headers.update(self.config.default_headers)
        headers.update(extra or {})
        return headers

    def _sleep(self, attempt: int, response: requests.Response | None = None) -> None:
        retry_after = response.headers.get("Retry-After") if response is not None else None
        if retry_after and retry_after.isdigit():
            delay = float(retry_after)
        else:
            delay = self.config.backoff_seconds * (2**attempt)
        if delay > 0:
            time.sleep(delay)
