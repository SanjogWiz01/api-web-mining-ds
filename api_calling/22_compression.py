"""
📘 TOPIC 22: Compression — Shrinking the Wire
===========================================
APIs often gzip/deflate JSON to save bandwidth.
Client advertises support with:
    Accept-Encoding: gzip, deflate, br

`requests` transparently decompresses gzip for you.
Check Content-Encoding to confirm compression happened.
"""

import requests
import gzip
import io

BASE_URL = "https://httpbin.org"


# ─────────────────────────────────────────────
# 1. Verify compression support
# ─────────────────────────────────────────────
def verify_compression():
    print("\n── Compression Headers ──────────────")
    r = requests.get(f"{BASE_URL}/gzip")
    print(f"  Status          : {r.status_code}")
    print(f"  Content-Encoding: {r.headers.get('content-encoding')}")
    print(f"  Body decoded OK : {r.json().get('gzipped')}")


# ─────────────────────────────────────────────
# 2. Compare size: raw JSON vs compressed
# ─────────────────────────────────────────────
def size_comparison():
    print("\n── Size Comparison ──────────────────")
    r = requests.get(f"{BASE_URL}/bytes/10000")
    raw = r.content
    compressed = gzip.compress(raw)
    ratio = (1 - len(compressed) / len(raw)) * 100
    print(f"  Raw bytes      : {len(raw)}")
    print(f"  Gzip bytes     : {len(compressed)}")
    print(f"  Space saved    : {ratio:.1f}%")


# ─────────────────────────────────────────────
# 3. Manually decompress if server sends raw gzip
# ─────────────────────────────────────────────
def manual_decompress():
    print("\n── Manual Decompress ────────────────")
    payload = b"web mining and api calling " * 500
    compressed = gzip.compress(payload)
    with gzip.GzipFile(fileobj=io.BytesIO(compressed)) as f:
        restored = f.read()
    print(f"  Restored == original? {restored == payload}")
    print(f"  {len(payload)} → {len(compressed)} bytes")


# ─────────────────────────────────────────────
# 4. Streaming a compressed response
# ─────────────────────────────────────────────
def stream_compressed():
    print("\n── Streaming + Compression ──────────")
    r = requests.get(f"{BASE_URL}/stream-bytes/4096", stream=True)
    r.raise_for_status()
    total = sum(len(chunk) for chunk in r.iter_content(chunk_size=512))
    print(f"  Streamed {total} bytes decompressed")
    print(f"  Encoding: {r.headers.get('content-encoding', 'identity')}")


if __name__ == "__main__":
    print("=" * 55)
    print("  COMPRESSION: gzip & friends")
    print("=" * 55)
    verify_compression()
    size_comparison()
    manual_decompress()
    stream_compressed()
    print("\nCompression demos complete.")