"""Real implementation: API monitoring & uptime checker.

Monitors a set of endpoints, measures latency, records response times, and
flags unhealthy services. Uses the same ideas as topic 30 in the Java folder
but fully async and thread-safe.

Run:
    pip install httpx
    python 27_api_monitoring.py
"""

import asyncio
import json
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from statistics import mean

import httpx


@dataclass
class HealthResult:
    endpoint: str
    status_code: int
    latency_ms: float
    healthy: bool
    checked_at: float = field(default_factory=time.time)


@dataclass
class EndpointStats:
    endpoint: str
    window: deque = field(default_factory=lambda: deque(maxlen=100))
    failures: int = 0

    @property
    def avg_latency_ms(self) -> float:
        return round(mean(r.latency_ms for r in self.window), 1) if self.window else 0.0

    @property
    def availability(self) -> float:
        if not self.window:
            return 0.0
        healthy = sum(1 for r in self.window if r.healthy)
        return round(healthy / len(self.window) * 100, 1)


class Monitor:
    def __init__(self, endpoints: list[str], *,
                 threshold_ms: int = 1000,
                 interval_s: float = 5.0):
        self.endpoints = endpoints
        self.threshold_ms = threshold_ms
        self.interval_s = interval_s
        self.stats: dict[str, EndpointStats] = {
            url: EndpointStats(endpoint=url) for url in endpoints
        }

    async def _check(self, client: httpx.AsyncClient, url: str) -> HealthResult:
        start = time.perf_counter()
        status = 0
        try:
            r = await client.get(url)
            status = r.status_code
        except httpx.HTTPError:
            status = 0  # network failure
        latency = (time.perf_counter() - start) * 1000
        healthy = (status in (200, 201, 204)) and latency < self.threshold_ms

        stat = self.stats[url]
        if not healthy:
            stat.failures += 1
        stat.window.append(HealthResult(url, status, round(latency, 1), healthy))
        return self.stats[url]

    async def run_once(self, client: httpx.AsyncClient) -> list[EndpointStats]:
        return [await self._check(client, url) for url in self.endpoints]

    async def run_forever(self, duration_s: float = 30.0) -> None:
        async with httpx.AsyncClient(timeout=10.0) as client:
            end = time.monotonic() + duration_s
            while time.monotonic() < end:
                stats = await self.run_once(client)
                for s in stats:
                    print(f"  {s.endpoint:<55} status={s.window[-1].status_code:>3} "
                          f"latency={s.window[-1].latency_ms:>8.1f}ms "
                          f"avg={s.avg_latency_ms:>8.1f}ms avail={s.availability}% "
                          f"healthy={s.window[-1].healthy}")
                await asyncio.sleep(self.interval_s)

    def report(self) -> dict:
        return {
            url: {
                "avg_latency_ms": stat.avg_latency_ms,
                "availability_pct": stat.availability,
                "failures": stat.failures,
                "samples": len(stat.window),
            }
            for url, stat in self.stats.items()
        }


async def main() -> None:
    monitor = Monitor(
        [
            "https://jsonplaceholder.typicode.com/posts/1",
            "https://jsonplaceholder.typicode.com/comments/1",
            "https://httpbin.org/delay/2",          # slow -> flagged unhealthy
            "https://httpbin.org/status/500",       # 500 -> flagged unhealthy
        ],
        threshold_ms=1500,
        interval_s=3.0,
    )
    await monitor.run_forever(duration_s=9)
    print("\n== final report ==")
    print(json.dumps(monitor.report(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())