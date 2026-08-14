"""
📘 TOPIC 9: Documentation — Read the Docs First
================================================
API documentation is your single source of truth.
80% of API issues are solved by reading the docs carefully.

Key sections to check in any API doc:
  1. Authentication methods (API key? OAuth? JWT?)
  2. Base URL and versioning (/v1/, /v2/)
  3. Endpoint reference (all available paths + methods)
  4. Request/response schema (field names, types, required/optional)
  5. Rate limits and quotas
  6. Error codes and their meanings
  7. Code examples (curl / Python / JavaScript)
  8. SDKs and client libraries

Popular free APIs with excellent documentation:
  - JSONPlaceholder   : https://jsonplaceholder.typicode.com/
  - OpenWeatherMap    : https://openweathermap.org/api
  - GitHub REST API   : https://docs.github.com/en/rest
  - NASA APIs         : https://api.nasa.gov/
  - The Dog API       : https://thedogapi.com/
  - REST Countries    : https://restcountries.com/
  - Open Library API  : https://openlibrary.org/developers/api
"""

import requests
import json


# ─────────────────────────────────────────────
# Exploring an API via its docs-documented routes
# We use JSONPlaceholder which has full docs
# ─────────────────────────────────────────────

API_DOCS_REFERENCE = {
    "Base URL": "https://jsonplaceholder.typicode.com",
    "Version": "N/A (implicit v1)",
    "Auth Required": "No (public API)",
    "Rate Limits": "None documented",
    "Endpoints": {
        "GET /posts":             "List all posts",
        "GET /posts/{id}":        "Get specific post",
        "POST /posts":            "Create new post",
        "PUT /posts/{id}":        "Update post (full replace)",
        "PATCH /posts/{id}":      "Update post (partial)",
        "DELETE /posts/{id}":     "Delete post",
        "GET /posts/{id}/comments": "Get comments for post",
        "GET /users":             "List all users",
        "GET /users/{id}":        "Get specific user",
        "GET /todos":             "List all todos",
        "GET /photos":            "List all photos",
        "GET /albums":            "List all albums",
    },
    "Request Schema (POST /posts)": {
        "title":  {"type": "string",  "required": True},
        "body":   {"type": "string",  "required": True},
        "userId": {"type": "integer", "required": True},
    },
}


def print_api_reference():
    print("\n── API Documentation Reference ──────")
    print(f"  Base URL : {API_DOCS_REFERENCE['Base URL']}")
    print(f"  Auth     : {API_DOCS_REFERENCE['Auth Required']}")
    print(f"  Limits   : {API_DOCS_REFERENCE['Rate Limits']}")
    print(f"\n  Available Endpoints:")
    for path, desc in API_DOCS_REFERENCE["Endpoints"].items():
        print(f"    {path:<35} → {desc}")

    print(f"\n  Request Schema for POST /posts:")
    for field, meta in API_DOCS_REFERENCE["Request Schema (POST /posts)"].items():
        req = "required" if meta["required"] else "optional"
        print(f"    {field:<10} : {meta['type']:<10}  [{req}]")


def explore_endpoints_from_docs():
    """Follow the documented endpoints exactly as shown in the API reference."""
    print("\n── Calling Documented Endpoints ─────")
    base = API_DOCS_REFERENCE["Base URL"]

    for path, desc in list(API_DOCS_REFERENCE["Endpoints"].items())[:5]:
        if "{id}" in path:
            url = f"{base}{path.replace('{id}', '1').split('/comments')[0]}"
            if "comments" in path:
                url = f"{base}/posts/1/comments"
        else:
            url = f"{base}{path}"

        r = requests.get(url, params={"_limit": 1} if not "{id}" in path else {})
        data = r.json()
        count = len(data) if isinstance(data, list) else 1
        print(f"  {desc:<35} [{r.status_code}] → {count} record(s)")


def schema_validation_from_docs():
    """Validate a response against the documented schema."""
    print("\n── Schema Validation (docs-guided) ──")
    base = API_DOCS_REFERENCE["Base URL"]
    schema = API_DOCS_REFERENCE["Request Schema (POST /posts)"]

    r = requests.get(f"{base}/posts/1")
    response_data = r.json()

    print(f"  Validating response against documented schema:")
    all_valid = True
    for field, meta in schema.items():
        value = response_data.get(field)
        expected_py_type = {"string": str, "integer": int}.get(meta["type"], object)
        is_present = value is not None
        is_type_ok = isinstance(value, expected_py_type) if is_present else False
        status = "OK" if (is_present and is_type_ok) else "FAIL"
        if status == "FAIL":
            all_valid = False
        print(f"    {field:<10} | present={is_present} | type_ok={is_type_ok} | [{status}]")

    print(f"  Overall validation: {'PASSED' if all_valid else 'FAILED'}")


if __name__ == "__main__":
    print("=" * 55)
    print("  DOCUMENTATION: Read API Docs Before Coding")
    print("=" * 55)
    print_api_reference()
    explore_endpoints_from_docs()
    schema_validation_from_docs()
    print("\nDocumentation demos complete.")
    print("\nTIP: Always open the API docs in a browser tab while coding!")
