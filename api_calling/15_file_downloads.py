"""
📘 TOPIC 15: File Downloads & Streaming
======================================
APIs can return binary files (PDF, ZIP, images).
Always stream large files and check the Content-Type header.

Use `stream=True` to avoid loading everything into memory.
"""

import requests
import io

BASE_URL = "https://httpbin.org"


# ─────────────────────────────────────────────
# 1. Download to memory
# ─────────────────────────────────────────────
def download_to_memory():
    print("\n── Download to Memory ───────────────")
    r = requests.get(f"{BASE_URL}/bytes/512")
    print(f"  Status      : {r.status_code}")
    print(f"  Content-Type: {r.headers.get('content-type')}")
    print(f"  Bytes       : {len(r.content)}")
    print(f"  First bytes : {r.content[:8].hex()}")


# ─────────────────────────────────────────────
# 2. Stream large download and write to disk
# ─────────────────────────────────────────────
def stream_to_disk():
    print("\n── Stream to Disk ───────────────────")
    r = requests.get(f"{BASE_URL}/stream-bytes/2048", stream=True)
    total = 0
    for chunk in r.iter_content(chunk_size=256):
        if chunk:
            total += len(chunk)
    print(f"  Streamed {total} bytes in chunks — no full buffer used")


# ─────────────────────────────────────────────
# 3. Save image/binary via io.BytesIO
# ─────────────────────────────────────────────
def binary_to_bytesio():
    print("\n── Binary via BytesIO ───────────────")
    r = requests.get(f"{BASE_URL}/image/png")
    buf = io.BytesIO(r.content)
    print(f"  Status      : {r.status_code}")
    print(f"  Content-Type: {r.headers.get('content-type')}")
    print(f"  Image size  : {buf.getbuffer().nbytes} bytes")
    print(f"  PNG header  : {buf.getvalue()[:8] == b'\\x89PNG\\r\\n\\x1a\\n'}")


# ─────────────────────────────────────────────
# 4. Check Content-Disposition filename
# ─────────────────────────────────────────────
def inspect_download_headers():
    print("\n── Download Headers ─────────────────")
    r = requests.get(f"{BASE_URL}/response-headers",
                     params={"Content-Disposition": 'attachment; filename="data.zip"'})
    cd = r.headers.get("content-disposition")
    print(f"  Content-Disposition: {cd}")


if __name__ == "__main__":
    print("=" * 55)
    print("  DOWNLOADS: binary files & streaming")
    print("=" * 55)
    download_to_memory()
    stream_to_disk()
    binary_to_bytesio()
    inspect_download_headers()
    print("\nDownload demos complete.")