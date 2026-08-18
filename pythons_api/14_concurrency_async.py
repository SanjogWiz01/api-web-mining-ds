"""Practice file: concurrency and async API calls.

Two approaches:
  1. ThreadPoolExecutor + requests   (I/O-bound parallelism, simple)
  2. asyncio + httpx/aiohttp         (native async, high throughput)

Run:  python 14_concurrency_async.py
"""

import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


URLS = [f"https://jsonplaceholder.typicode.com/posts/{i}" for i in range(1, 21)]


def fetch_one(url: str) -> tuple[str, int]:
    r = requests.get(url, timeout=(5, 15))
    r.raise_for_status()
    return url, r.status_code


def sequential() -> float:
    print("== sequential ==")
    start = time.perf_counter()
    for url in URLS:
        fetch_one(url)
    elapsed = time.perf_counter() - start
    print(f"  {len(URLS)} requests in {elapsed:.2f}s")
    return elapsed


def threaded() -> float:
    print("== ThreadPoolExecutor ==")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=10) as pool:
        futures = [pool.submit(fetch_one, url) for url in URLS]
        for future in as_completed(futures):
            _, status = future.result()
            assert status == 200
    elapsed = time.perf_counter() - start
    print(f"  {len(URLS)} requests in {elapsed:.2f}s")
    return elapsed


async def async_version() -> float:
    print("== asyncio + httpx ==")
    import httpx

    async with httpx.AsyncClient(timeout=10.0) as client:
        async def get_one(url: str) -> None:
            r = await client.get(url)
            r.raise_for_status()

        start = time.perf_counter()
        await asyncio.gather(*(get_one(u) for u in URLS))
        elapsed = time.perf_counter() - start
        print(f"  {len(URLS)} requests in {elapsed:.2f}s")
        return elapsed


async def aiohttp_version() -> float:
    print("== asyncio + aiohttp ==")
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async def get_one(url: str) -> None:
            async with session.get(url) as r:
                r.raise_for_status()

        start = time.perf_counter()
        await asyncio.gather(*(get_one(u) for u in URLS))
        elapsed = time.perf_counter() - start
        print(f"  {len(URLS)} requests in {elapsed:.2f}s")
        return elapsed


if __name__ == "__main__":
    t_seq = sequential()
    t_thr = threaded()
    t_async = asyncio.run(async_version())
    t_aio = asyncio.run(aiohttp_version())
    print("\nsummary:")
    print(f"  sequential : {t_seq:5.2f}s")
    print(f"  threaded   : {t_thr:5.2f}s")
    print(f"  httpx async: {t_async:5.2f}s")
    print(f"  aiohttp    : {t_aio:5.2f}s")
