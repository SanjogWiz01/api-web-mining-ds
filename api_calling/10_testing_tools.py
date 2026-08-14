"""
📘 TOPIC 10: Testing Tools — Postman & curl Before Coding
=========================================================
Before writing application code, always test API endpoints manually.
This saves hours of debugging later.

Tools:
  curl    → Command-line HTTP client (built into Linux/macOS/Windows)
  Postman → GUI tool for testing APIs (free at https://postman.com)
  httpie  → User-friendly CLI alternative to curl
  Insomnia→ Another GUI client (alternative to Postman)

In Python, we can also generate curl-equivalent commands from requests
and create automated test scripts.
"""

import requests
import json
import time


BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Generate curl commands from Python requests
# ─────────────────────────────────────────────
def generate_curl_command(method: str, url: str, headers: dict = None,
                           data: dict = None, params: dict = None) -> str:
    """Generate an equivalent curl command string for a given request config."""
    parts = [f"curl -X {method.upper()}"]

    if headers:
        for k, v in headers.items():
            parts.append(f'-H "{k}: {v}"')

    if data:
        json_data = json.dumps(data)
        parts.append(f"-d '{json_data}'")

    if params:
        query = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query}"

    parts.append(f'"{url}"')
    return " \\\n  ".join(parts)


def show_curl_equivalents():
    print("\n── curl Equivalent Commands ─────────")

    # GET
    cmd = generate_curl_command("GET", f"{BASE_URL}/posts/1")
    print(f"\n  [GET single post]\n  {cmd}")

    # GET with params
    cmd = generate_curl_command("GET", f"{BASE_URL}/posts",
                                params={"userId": 1, "_limit": 3})
    print(f"\n  [GET with query params]\n  {cmd}")

    # POST with JSON
    cmd = generate_curl_command(
        "POST", f"{BASE_URL}/posts",
        headers={"Content-Type": "application/json", "Authorization": "Bearer TOKEN"},
        data={"title": "Test", "body": "Hello", "userId": 1}
    )
    print(f"\n  [POST with JSON body]\n  {cmd}")

    # DELETE
    cmd = generate_curl_command("DELETE", f"{BASE_URL}/posts/1")
    print(f"\n  [DELETE]\n  {cmd}")


# ─────────────────────────────────────────────
# 2. Automated Test Suite (pre-coding validation)
# ─────────────────────────────────────────────
class APITestSuite:
    """Lightweight API test runner — use this BEFORE writing feature code."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []

    def run_test(self, name: str, method: str, path: str,
                 expected_status: int, payload: dict = None,
                 expected_keys: list = None):
        url = f"{self.base_url}{path}"
        try:
            r = getattr(requests, method.lower())(url, json=payload, timeout=10)
            status_ok = r.status_code == expected_status

            keys_ok = True
            if expected_keys and r.status_code < 300:
                data = r.json()
                if isinstance(data, list):
                    data = data[0] if data else {}
                keys_ok = all(k in data for k in expected_keys)

            passed = status_ok and keys_ok
            self.results.append({"name": name, "passed": passed,
                                  "status": r.status_code, "expected": expected_status})
            icon = "PASS" if passed else "FAIL"
            print(f"  [{icon}] {name:<40} | {r.status_code} (expected {expected_status})")
        except Exception as e:
            self.results.append({"name": name, "passed": False, "error": str(e)})
            print(f"  [ERR]  {name:<40} | Exception: {e}")

    def summary(self):
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        print(f"\n  Results: {passed}/{total} tests passed")


def run_api_test_suite():
    print("\n── Automated API Test Suite ─────────")
    suite = APITestSuite(BASE_URL)

    suite.run_test("GET /posts returns 200",
                   "GET", "/posts", 200, expected_keys=["id", "title", "userId"])

    suite.run_test("GET /posts/1 returns 200",
                   "GET", "/posts/1", 200, expected_keys=["id", "title", "body"])

    suite.run_test("GET nonexistent /posts/99999 returns 404",
                   "GET", "/posts/99999", 404)

    suite.run_test("POST /posts returns 201",
                   "POST", "/posts", 201,
                   payload={"title": "Test", "body": "Body", "userId": 1},
                   expected_keys=["id", "title"])

    suite.run_test("DELETE /posts/1 returns 200",
                   "DELETE", "/posts/1", 200)

    suite.run_test("GET /users returns 200",
                   "GET", "/users", 200, expected_keys=["id", "name", "email"])

    suite.summary()


# ─────────────────────────────────────────────
# 3. Postman Collection Export Format
# ─────────────────────────────────────────────
def show_postman_workflow():
    print("\n── Postman Testing Workflow ─────────")
    steps = [
        ("1", "Open Postman → New Collection → 'My API Tests'"),
        ("2", "Add Environment: BASE_URL = https://jsonplaceholder.typicode.com"),
        ("3", "New Request: GET {{BASE_URL}}/posts/1 → Send → Inspect response"),
        ("4", "Add Test Script in 'Tests' tab:"),
        ("",  "    pm.test('Status 200', () => pm.response.to.have.status(200));"),
        ("",  "    pm.test('Has title', () => { const data = pm.response.json(); pm.expect(data.title).to.be.a('string'); });"),
        ("5", "Save request → Run Collection → View results"),
        ("6", "Export collection as JSON → Share with team"),
    ]
    for num, step in steps:
        prefix = f"  Step {num}:" if num else "         "
        print(f"{prefix} {step}")


if __name__ == "__main__":
    print("=" * 55)
    print("  TESTING TOOLS: curl + Postman + Automated Tests")
    print("=" * 55)
    show_curl_equivalents()
    run_api_test_suite()
    show_postman_workflow()
    print("\nTesting tools demos complete.")
    print("\nTIP: Run this test suite against any new API before writing prod code!")
