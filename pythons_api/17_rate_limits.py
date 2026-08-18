"""Practice file: client-side rate limiting.

Be a good API citizen: throttle your own requests, honor Retry-After, and
pause between bursts.

Run:  python 17_rate_limits.py
"""

import threading
import time
from collections import deque

import requests


class RateLimiter:
    """Token-bucket style limiter using a sliding window."""

    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self._calls: deque[float] = deque()
        self._lock = threading.Lock()

    def wait_if_needed(self) -> None:
        with self._lock:
            now = time.monotonic()
            while self._calls and now - self._calls[0] > self.period:
                self._calls.popleft()

            if len(self._calls) >= self.max_calls:
                wait = self.period - (now - self._calls[0])
                print(f"  throttled: waiting {wait:.2f}s")
                time.sleep(wait)

            self._calls.append(time.monotonic())


def honor_retry_after(response: requests.Response) -> float:
    """Extract Retry-After (seconds or HTTP-date) from a 429 response."""
    raw = response.headers.get("Retry-After")
    if raw is None:
        return 1.0
    try:
        return max(0.0, float(raw))
    except ValueError:
        import email.utils
        parsed = email.utils.parsedate_to_datetime(raw)
        delta = parsed - email.utils.parsedate_to_datetime(response.headers.get("Date"))
        return max(0.0, delta.total_seconds())


def demo_rate_limiter() -> None:
    print("== sliding window limiter (5 calls / 2s) ==")
    limiter = RateLimiter(max_calls=5, period=2.0)
    start = time.perf_counter()
    for i in range(12):
        limiter.wait_if_needed()
        print(f"  call {i + 1} at t={time.perf_counter() - start:.2f}s")
        # no real network here; call the limiter on a harmless endpoint
    print(f"  finished in {time.perf_counter() - start:.2f}s")


def demo_retry_after() -> None:
    print("== honor Retry-After ==")
    r = requests.get("https://httpbin.org/response-headers",
                     params={"Retry-After": "2", "Date": time.strftime("%a, %d %b %Y %H:%M:%S GMT")},
                     timeout=(3, 10))
    wait = honor_retry_after(r)
    print(f"  computed wait: {wait}s")


def demo_status_429() -> None:
    print("== real 429 from httpbin ==")
    r = requests.get("https://httpbin.org/status/429", timeout=(3, 10))
    print(f"  status={r.status_code}, retry-after={r.headers.get('Retry-After')}")


if __name__ == "__main__":
    demo_rate_limiter()
    demo_retry_after()
    demo_status_429()
