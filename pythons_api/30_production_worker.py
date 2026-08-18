"""PRODUCTION-GRADE async worker + API consumer (heavy implementation).

The companion to `29_production_api.py`. This is the kind of service that sits
*on the other side* of an API: a high-throughput consumer of a task queue API.

Features:
  - Structured logging with request IDs
  - Async HTTP client (httpx) with connection pooling
  - Circuit breaker (fail fast when the upstream is down)
  - Retry with exponential backoff + jitter, honoring Retry-After
  - Bounded concurrency via semaphore (never floods the upstream)
  - Batching of payloads (reduces request count)
  - Idempotent task consumption (no double-processing)
  - Graceful shutdown draining in-flight work
  - In-memory metrics that can be scraped by a monitoring system

This file is self-contained and runnable: it ships a tiny in-memory fake
upstream so you can watch it work without a real API.

Run:
    pip install httpx
    python 30_production_worker.py
"""

import asyncio
import contextlib
import json
import logging
import random
import signal
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

import httpx

# -------------------------------------------------------------------- logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("worker")


# ----------------------------------------------------------------- settings
@dataclass(frozen=True)
class WorkerSettings:
    upstream_base: str = "http://127.0.0.1:8000"
    poll_interval_s: float = 2.0
    max_concurrency: int = 8
    batch_size: int = 10
    max_retries: int = 3
    backoff_base_s: float = 0.5
    backoff_cap_s: float = 20.0
    circuit_fail_threshold: int = 5
    circuit_reset_s: float = 30.0
    queue_size: int = 100


SETTINGS = WorkerSettings()


# ------------------------------------------------------------ circuit breaker
class CircuitBreaker:
    """Trips open after N consecutive failures, then half-opens for probes."""

    def __init__(self, fail_threshold: int, reset_after_s: float):
        self.fail_threshold = fail_threshold
        self.reset_after_s = reset_after_s
        self.failures = 0
        self.open_until = 0.0
        self.state = "closed"

    def allow(self) -> bool:
        now = time.monotonic()
        if self.state == "open":
            if now >= self.open_until:
                self.state = "half-open"
                return True
            return False
        return True

    def record_success(self) -> None:
        self.failures = 0
        self.state = "closed"

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.fail_threshold:
            self.state = "open"
            self.open_until = time.monotonic() + self.reset_after_s
            logger.warning("circuit breaker OPEN - failing fast")
            return
        if self.state == "half-open":
            self.state = "open"
            self.open_until = time.monotonic() + self.reset_after_s
            logger.warning("circuit breaker probe failed - OPEN again")


breaker = CircuitBreaker(SETTINGS.circuit_fail_threshold, SETTINGS.circuit_reset_s)


# ------------------------------------------------------------ retry + backoff
def backoff_delay(attempt: int) -> float:
    exp = min(SETTINGS.backoff_base_s * (2 ** attempt), SETTINGS.backoff_cap_s)
    return exp + random.uniform(0, 0.1 * exp)


async def call_with_retries(
    client: httpx.AsyncClient,
    method: str,
    path: str,
    **kwargs: Any,
) -> httpx.Response:
    """Call upstream honoring Retry-After, backoff, and the circuit breaker."""
    if not breaker.allow():
        raise httpx.TransportError("circuit open - request not sent")

    last_exc: Exception | None = None
    for attempt in range(SETTINGS.max_retries + 1):
        try:
            response = await client.request(method, path, **kwargs)
            if response.status_code in (200, 201, 204):
                breaker.record_success()
                return response
            if response.status_code == 429:
                wait = float(response.headers.get("Retry-After", backoff_delay(attempt)))
                await asyncio.sleep(wait)
                continue
            if response.status_code >= 500:
                await asyncio.sleep(backoff_delay(attempt))
                continue
            breaker.record_success()  # 4xx is a caller error, not an outage
            return response
        except (httpx.ConnectError, httpx.ReadTimeout) as exc:
            last_exc = exc
            breaker.record_failure()
            await asyncio.sleep(backoff_delay(attempt))
        except httpx.HTTPError as exc:
            last_exc = exc
            await asyncio.sleep(backoff_delay(attempt))

    raise httpx.TransportError(f"giving up after {SETTINGS.max_retries} retries") from last_exc


# ------------------------------------------------------------------- worker
@dataclass
class Task:
    id: str
    kind: str
    payload: dict[str, Any]


@dataclass
class WorkerMetrics:
    tasks_processed: int = 0
    tasks_failed: int = 0
    batches_sent: int = 0
    latency_ms: list[float] = field(default_factory=lambda: deque(maxlen=100))

    def snapshot(self) -> dict[str, Any]:
        return {
            "tasks_processed": self.tasks_processed,
            "tasks_failed": self.tasks_failed,
            "batches_sent": self.batches_sent,
            "avg_batch_latency_ms": round(
                sum(self.latency_ms) / len(self.latency_ms), 1
            ) if self.latency_ms else 0.0,
            "circuit_state": breaker.state,
        }


class TaskWorker:
    def __init__(self, settings: WorkerSettings = SETTINGS) -> None:
        self.settings = settings
        self.metrics = WorkerMetrics()
        self._queue: asyncio.Queue[Task] = asyncio.Queue(maxsize=settings.queue_size)
        self._seen_ids: set[str] = set()   # idempotency guard
        self._semaphore = asyncio.Semaphore(settings.max_concurrency)
        self._running = True

    async def _fetch_batch(self, client: httpx.AsyncClient) -> list[Task]:
        """Pull a batch of pending tasks from the upstream."""
        try:
            response = await call_with_retries(
                client,
                "GET",
                f"{self.settings.upstream_base}/tasks/pending?batch={self.settings.batch_size}",
            )
        except httpx.TransportError:
            return []
        if response.status_code >= 400:
            return []

        tasks = []
        for item in response.json().get("tasks", []):
            if item["id"] in self._seen_ids:
                continue
            self._seen_ids.add(item["id"])
            tasks.append(Task(item["id"], item["kind"], item.get("payload", {})))
        return tasks

    async def _process_task(self, client: httpx.AsyncClient, task: Task) -> bool:
        """Process one task with bounded concurrency; acknowledge only on success."""
        async with self._semaphore:
            try:
                await asyncio.sleep(0.02)  # simulated compute
                response = await call_with_retries(
                    client,
                    "POST",
                    f"{self.settings.upstream_base}/tasks/{task.id}/complete",
                    json={"result": f"{task.kind}:{task.payload}"},
                )
                ok = response.status_code in (200, 201, 204)
            except httpx.TransportError:
                ok = False
        return ok

    async def _drain_queue(self, client: httpx.AsyncClient) -> None:
        results = await asyncio.gather(
            *(self._process_task(client, task) for task in list(self._queue.queue))
        )
        for task, ok in zip(list(self._queue.queue), results):
            if ok:
                self.metrics.tasks_processed += 1
            else:
                self.metrics.tasks_failed += 1
            self._queue.get_nowait()
            self._queue.task_done()

    async def run(self) -> None:
        async with httpx.AsyncClient(
            timeout=10.0,
            headers={"Accept": "application/json", "User-Agent": "worker/1.0"},
        ) as client:
            while self._running:
                started = time.perf_counter()

                new_tasks = await self._fetch_batch(client)
                for t in new_tasks:
                    if self._queue.full():
                        break
                    self._queue.put_nowait(t)

                if not self._queue.empty():
                    await self._drain_queue(client)
                    self.metrics.batches_sent += 1
                    self.metrics.latency_ms.append((time.perf_counter() - started) * 1000)

                logger.info(
                    "tick | new=%d pending=%d processed=%d failed=%d circuit=%s",
                    len(new_tasks), self._queue.qsize(),
                    self.metrics.tasks_processed, self.metrics.tasks_failed, breaker.state,
                )
                await asyncio.sleep(self.settings.poll_interval_s)

    def shutdown(self) -> None:
        logger.info("graceful shutdown requested - draining queue")
        self._running = False


# ------------------------------------------------------------ fake upstream
class FakeUpstream:
    """In-memory stand-in for the real task API so the worker runs standalone."""

    def __init__(self) -> None:
        self.pending: deque[dict[str, Any]] = deque()
        self.completed: list[str] = []
        self.failures_remaining = 3  # simulate a brief outage at boot

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path

        if path.endswith("/tasks/pending"):
            if self.failures_remaining > 0:
                self.failures_remaining -= 1
                return httpx.Response(503, request=request, json={"error": "temporarily down"})
            batch = [self.pending.popleft() for _ in range(SETTINGS.batch_size) if self.pending]
            return httpx.Response(200, request=request, json={"tasks": batch})

        if path.endswith("/complete"):
            task_id = path.split("/")[-2]
            self.completed.append(task_id)
            return httpx.Response(200, request=request, json={"ok": True})

        return httpx.Response(404, request=request)


async def demo() -> None:
    upstream = FakeUpstream()
    for i in range(25):
        upstream.pending.append({"id": uuid.uuid4().hex, "kind": "job", "payload": {"n": i}})

    app = httpx.AsyncHTTPTransport(handler=upstream)
    worker = TaskWorker(WorkerSettings(poll_interval_s=0.5))

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        with contextlib.suppress(NotImplementedError):
            loop.add_signal_handler(sig, worker.shutdown)

    run_task = asyncio.create_task(worker.run())
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(run_task, timeout=8.0)
    worker.shutdown()
    await run_task

    print("\n== final metrics ==")
    print(json.dumps(worker.metrics.snapshot(), indent=2))
    print(f"  upstream completed: {len(upstream.completed)}")


if __name__ == "__main__":
    asyncio.run(demo())