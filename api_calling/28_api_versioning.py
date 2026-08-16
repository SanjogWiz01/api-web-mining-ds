"""
📘 TOPIC 28: API Versioning — Never Break Your Users
===================================================
APIs change. Versioning lets you evolve without breaking clients.

Common strategies:
  URL path      → /v1/users, /v2/users
  Query param   → ?version=2
  Header        → Accept: application/vnd.myapi.v2+json
  Date          → /2025-01-01/users (Stripe-style)

"""

import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Version in the URL path
# ─────────────────────────────────────────────
def url_versioning():
    print("\n── URL Path Versioning ──────────────")
    for v in ("v1", "v2"):
        url = f"{BASE_URL}/{v}/posts/1"  # demo pattern
        r = requests.get(url)
        print(f"  GET {url} → {r.status_code}")
    print("  Common: /api/v1/users, /api/v2/users")


# ─────────────────────────────────────────────
# 2. Version via Accept header (media type)
# ─────────────────────────────────────────────
def header_versioning():
    print("\n── Accept Header Versioning ─────────")
    headers = {"Accept": "application/vnd.myapi.v2+json"}
    r = requests.get(f"{BASE_URL}/posts/1", headers=headers)
    print(f"  Accept: {headers['Accept']}")
    print(f"  Status: {r.status_code}")
    print("  Server picks the handler matching the media type")


# ─────────────────────────────────────────────
# 3. Choose the right version
# ─────────────────────────────────────────────
def version_selection():
    print("\n── Version Selection ────────────────")
    print("  Use the latest stable version unless you need:")
    print("    • deprecated fields")
    print("    • old behavior guaranteed by contract")
    print("  Set a version constant in your client config.")


# ─────────────────────────────────────────────
# 4. Deprecation headers
# ─────────────────────────────────────────────
def deprecation_headers():
    print("\n── Deprecation Signals ──────────────")
    headers = {
        "Deprecation": "Tue, 31 Dec 2025 23:59:59 GMT",
        "Sunset": "Wed, 30 Apr 2026 00:00:00 GMT",
        "Link": '<https://api.example.com/v2>; rel="successor-version"',
    }
    for k, v in headers.items():
        print(f"  {k:<14} {v}")
    print("  → Listen for these and migrate before Sunset.")


if __name__ == "__main__":
    print("=" * 55)
    print("  API VERSIONING: evolve without breaking")
    print("=" * 55)
    url_versioning()
    header_versioning()
    version_selection()
    deprecation_headers()
    print("\nVersioning demos complete.")