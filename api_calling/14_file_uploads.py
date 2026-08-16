"""
📘 TOPIC 14: File Uploads — Multipart/form-data
==============================================
To send files to an API you POST multipart/form-data.
The `requests` library does this with the `files=` argument.

Format:
    files = {"field_name": ("filename.ext", file_obj, "mime/type")}
"""

import requests

BASE_URL = "https://httpbin.org"


# ─────────────────────────────────────────────
# 1. Upload a file from disk
# ─────────────────────────────────────────────
def upload_file_from_disk():
    print("\n── Upload From Disk ─────────────────")
    with open(__file__, "rb") as f:
        r = requests.post(f"{BASE_URL}/post", files={"file": ("topic_14.py", f, "text/x-python")})
    print(f"  Status: {r.status_code}")
    data = r.json()
    print(f"  Uploaded filename: {data.get('files', {}).get('file')}")


# ─────────────────────────────────────────────
# 2. Upload from bytes (in-memory)
# ─────────────────────────────────────────────
def upload_from_bytes():
    print("\n── Upload From Bytes ────────────────")
    content = b"hello api world\n" * 10
    r = requests.post(f"{BASE_URL}/post", files={"note": ("note.txt", content, "text/plain")})
    data = r.json()
    print(f"  Status: {r.status_code}")
    print(f"  Echoed note: {data.get('files', {}).get('note')}")


# ─────────────────────────────────────────────
# 3. Send file + JSON fields together
# ─────────────────────────────────────────────
def upload_with_fields():
    print("\n── File + Fields ────────────────────")
    r = requests.post(
        f"{BASE_URL}/post",
        data={"title": "Uploaded Report", "tags": "api,mining"},
        files={"report": ("report.pdf", b"%PDF-1.4 fake pdf", "application/pdf")},
    )
    data = r.json()
    print(f"  Status : {r.status_code}")
    print(f"  Form   : {data.get('form')}")
    print(f"  Files  : {list(data.get('files', {}).keys())}")


# ─────────────────────────────────────────────
# 4. Stream a large file upload
# ─────────────────────────────────────────────
def streaming_upload():
    print("\n── Streaming Upload ─────────────────")
    # generator-based upload streams data instead of loading it fully
    def chunks(chunk_size=1024):
        payload = b"x" * (4 * 1024)  # 4KB
        for i in range(0, len(payload), chunk_size):
            yield payload[i:i + chunk_size]

    r = requests.post(f"{BASE_URL}/post", data={"name": "stream"}, files={"blob": ("blob.bin", chunks(), "application/octet-stream")})
    print(f"  Status: {r.status_code} — streamed upload OK")


if __name__ == "__main__":
    print("=" * 55)
    print("  FILE UPLOADS: multipart/form-data")
    print("=" * 55)
    upload_file_from_disk()
    upload_from_bytes()
    upload_with_fields()
    streaming_upload()
    print("\nFile upload demos complete.")