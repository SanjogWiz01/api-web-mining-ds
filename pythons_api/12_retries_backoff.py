"""Practice file: retries with exponential backoff + jitter.

Transient failures (429, 5xx, timeouts) deserve retries. The correct backoff
grows exponentially and adds random jitter so retrying clients don't
synchronize (thundering herd).

Run:  python 12_retries_backoff.py
"""

import random
import time
from typing import Callable

import requests


def backoff_delay(attempt: int, base: float = 0.5, cap: float = 30.0,
                  jitter: float = 0.1) -> float:
    """Exponential backoff: base * 2^attempt, capped, with jitter."""
    delay = min(base * (2 ** attempt), cap)
    delay += random.uniform(0, jitter * delay)
    return delay


def retry_request(url: str, *, max_retries: int = 4) -> requests.Response:
    """Retry GET on 429/5xx/network errors using backoff_delay."""
    last_exc: Exception | None = None

    for attempt in range(max_retries + 1):
        try:
            r = requests.get(url, timeout=(3, 10))
            if r.status_code in (200, 201, 204):
                return r
            if r.status_code == 429:
                # honor the server's Retry-After when present
                wait = float(r.headers.get("Retry-After", backoff_delay(attempt)))
            elif r.status_code >= 500:
                wait = backoff_delay(attempt)
            else:
                r.raise_for_status()  # 4xx (not 429) -> fail fast, no retry

        except (requests.ConnectionError, requests.Timeout) as exc:
            last_exc = exc
            wait = backoff_delay(attempt)

        if attempt >= max_retries:
            raise RuntimeError(f"request failed after {max_retries} retries") from last_exc

        print(f"  attempt {attempt + 1} failed -> waiting {wait:.2f}s")
        time.sleep(wait)

    raise RuntimeError("unreachable")


def with_tenacity(func: Callable[[str], requests.Response], url: str) -> requests.Response:
    """Illustration: the `tenacity` library makes this declarative."""
    from tenacity import (
        retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
        retry_if_status_code,
    )
    import requests as _r

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.2, max=2),
        retry=retry_if_exception_type((_r.ConnectionError, _r.Timeout))
        | retry_if_status_code(429),
    )
    def call():
        return func(url)

    return call()


def demo() -> None:
    print("== simulated 503 with backoff ==")
    try:
        retry_request("https://httpbin.org/status/503", max_retries=3)
    except RuntimeError as e:
        print(f"  {e}")

    print("== happy path ==")
    r = retry_request("https://jsonplaceholder.typicode.com/posts/1")
    print(f"  got status {r.status_code}")

    print("== tenacity style ==")
    r = with_tenacity(lambda u: requests.get(u, timeout=(3, 10)),
                      "https://jsonplaceholder.typicode.com/posts/1")
    print(f"  got status {r.status_code}")


if __name__ == "__main__":
    demo()
