"""Async collection helpers for APIs that allow concurrent reads."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class AsyncApiConfig:
    timeout: float = 10.0
    user_agent: str = "api-web-mining-ds/0.1.0"
    concurrency: int = 5


async def fetch_json_many(
    urls: list[str],
    *,
    config: AsyncApiConfig | None = None,
    headers: dict[str, str] | None = None,
) -> list[Any]:
    """Fetch many JSON URLs concurrently while keeping a small concurrency cap."""

    import asyncio

    cfg = config or AsyncApiConfig()
    semaphore = asyncio.Semaphore(cfg.concurrency)
    request_headers = {"User-Agent": cfg.user_agent}
    request_headers.update(headers or {})

    async with httpx.AsyncClient(timeout=cfg.timeout, headers=request_headers) as client:
        async def fetch_one(url: str) -> Any:
            async with semaphore:
                response = await client.get(url)
                response.raise_for_status()
                return response.json()

        return await asyncio.gather(*(fetch_one(url) for url in urls))
