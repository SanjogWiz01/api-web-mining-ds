"""
📘 TOPIC 5: Error Handling — HTTP Status Codes
===============================================
Every HTTP response includes a status code telling you what happened.

  2xx — SUCCESS
    200 OK             → Request succeeded
    201 Created        → Resource was created (POST success)
    204 No Content     → Success, no body returned (DELETE)

  3xx — REDIRECT
    301 Moved Permanently  → Resource moved to a new URL
    304 Not Modified       → Cached version is still valid

  4xx — CLIENT ERRORS (your fault)
    400 Bad Request    → Malformed request or invalid data
    401 Unauthorized   → Authentication required or failed
    403 Forbidden      → Authenticated but not allowed
    404 Not Found      → Resource does not exist
    429 Too Many Reqs  → Rate limit exceeded

  5xx — SERVER ERRORS (their fault)
    500 Internal Error → Server crashed
    502 Bad Gateway    → Upstream server issue
    503 Unavailable    → Server overloaded or maintenance
"""

import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def check_status(response: requests.Response, context: str):
    code = response.status_code
    if 200 <= code < 300:
        print(f"  [{code}] SUCCESS: {context}")
    elif code == 400:
        print(f"  [{code}] BAD REQUEST: {context} — Check your payload/params")
    elif code == 401:
        print(f"  [{code}] UNAUTHORIZED: {context} — Invalid or missing token")
    elif code == 403:
        print(f"  [{code}] FORBIDDEN: {context} — You lack permission")
    elif code == 404:
        print(f"  [{code}] NOT FOUND: {context} — Resource doesn't exist")
    elif code == 429:
        retry_after = response.headers.get("Retry-After", "unknown")
        print(f"  [{code}] RATE LIMITED: Retry after {retry_after} seconds")
    elif code >= 500:
        print(f"  [{code}] SERVER ERROR: {context} — Not your fault, try later")
    else:
        print(f"  [{code}] UNKNOWN: {context}")


def safe_api_call(url: str, **kwargs) -> dict:
    """Wrapper with full error handling and exception catching."""
    try:
        response = requests.get(url, timeout=10, **kwargs)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
        return {"success": True, "data": response.json(), "status": response.status_code}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out after 10s"}

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Network connection failed"}

    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": str(e), "status": e.response.status_code}

    except requests.exceptions.JSONDecodeError:
        return {"success": False, "error": "Response was not valid JSON"}


def demo_error_handling():
    print("=" * 55)
    print("  ERROR HANDLING: Status Codes + Exception Safety")
    print("=" * 55)

    # ── 200 OK ────────────────────────────────
    print("\n── Simulating Response Codes ────────")
    r = requests.get(f"{BASE_URL}/posts/1")
    check_status(r, "GET /posts/1")

    # ── 201 Created ───────────────────────────
    r = requests.post(f"{BASE_URL}/posts", json={"title": "Test", "body": "X", "userId": 1})
    check_status(r, "POST /posts (create)")

    # ── 404 Not Found ─────────────────────────
    r = requests.get(f"{BASE_URL}/posts/99999")
    check_status(r, "GET /posts/99999 (nonexistent)")

    # ── Safe Wrapper Demo ─────────────────────
    print("\n── Safe API Call Wrapper ────────────")
    result = safe_api_call(f"{BASE_URL}/posts/1")
    print(f"  Success: {result['success']}")
    if result["success"]:
        print(f"  Title  : {result['data'].get('title', 'N/A')[:50]}")

    result = safe_api_call(f"{BASE_URL}/posts/99999")
    print(f"\n  Success: {result['success']}")
    print(f"  Error  : {result.get('error', 'N/A')}")
    print(f"  Status : {result.get('status', 'N/A')}")

    # ── raise_for_status() pattern ────────────
    print("\n── raise_for_status() Pattern ───────")
    try:
        r = requests.get(f"{BASE_URL}/posts/99999")
        r.raise_for_status()
        print(f"  Data: {r.json()}")
    except requests.exceptions.HTTPError as e:
        print(f"  HTTPError caught: {e}")
        print(f"  Status Code: {e.response.status_code}")

    print("\nError handling demos complete.")


if __name__ == "__main__":
    demo_error_handling()
