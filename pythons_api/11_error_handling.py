"""Practice file: robust error handling for API calls.

Builds a small client that never crashes on a bad response and always
distinguishes the failure type.

Run:  python 11_error_handling.py
"""

import json
import time

import requests


class ApiError(Exception):
    """Base class for API errors."""


class NetworkError(ApiError):
    pass


class TimeoutError(ApiError):
    pass


class RateLimitedError(ApiError):
    def __init__(self, retry_after: float):
        super().__init__(f"rate limited; retry after {retry_after}s")
        self.retry_after = retry_after


class HttpError(ApiError):
    def __init__(self, status_code: int, body: str):
        super().__init__(f"HTTP {status_code}: {body[:200]}")
        self.status_code = status_code
        self.body = body


def call_api(url: str, retries: int = 3) -> dict:
    """Robust GET that classifies failures as exceptions."""
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=(3, 10))
        except requests.ConnectionError as exc:
            raise NetworkError(f"could not connect to {url}") from exc
        except requests.Timeout as exc:
            raise TimeoutError(f"request to {url} timed out") from exc
        except requests.RequestException as exc:
            raise ApiError(f"request failed: {exc}") from exc

        if r.status_code == 429:
            retry_after = float(r.headers.get("Retry-After", 1))
            if attempt < retries - 1:
                time.sleep(retry_after)
                continue
            raise RateLimitedError(retry_after)
        if r.status_code >= 400:
            raise HttpError(r.status_code, r.text)

        try:
            return r.json()
        except json.JSONDecodeError as exc:
            raise ApiError("response was not valid JSON") from exc
    raise ApiError("unreachable")  # defensive


def demo() -> None:
    print("== happy path ==")
    data = call_api("https://jsonplaceholder.typicode.com/posts/1")
    print(f"  id={data['id']}, title={data['title'][:30]}...")

    print("== 404 -> HttpError ==")
    try:
        call_api("https://jsonplaceholder.typicode.com/posts/999999")
    except HttpError as e:
        print(f"  caught HttpError: {e.status_code}")

    print("== 500 series -> retried then raised ==")
    try:
        call_api("https://httpbin.org/status/503", retries=2)
    except HttpError as e:
        print(f"  caught HttpError after retries: status={e.status_code}")

    print("== connection failure -> NetworkError ==")
    try:
        call_api("http://127.0.0.1:1/none", retries=1)
    except NetworkError as e:
        print(f"  caught NetworkError: {type(e).__name__}")


if __name__ == "__main__":
    demo()
