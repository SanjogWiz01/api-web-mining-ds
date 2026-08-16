"""
📘 TOPIC 32: Contract Testing — Schema Validation
================================================
An API contract is the agreed shape of requests/responses.
Validate responses against the schema so breakages surface early.

Tools:
  jsonschema  → validate dicts against JSON Schema
  OpenAPI/Swagger → machine-readable contract
  pact       → consumer-driven contract testing
"""

import requests
import jsonschema

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. JSON Schema for a user object
# ─────────────────────────────────────────────
USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "address", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "address": {"type": "object"},
        "company": {"type": "object"},
    },
    "additionalProperties": True,
}


def validate_contract():
    print("\n── Validate Against Schema ──────────")
    r = requests.get(f"{BASE_URL}/users/1")
    user = r.json()
    try:
        jsonschema.validate(user, USER_SCHEMA)
        print(f"  ✓ /users/1 conforms to schema")
    except jsonschema.ValidationError as e:
        print(f"  ✗ Contract violated: {e.message}")


# ─────────────────────────────────────────────
# 2. Broken contract detection
# ─────────────────────────────────────────────
def broken_contract():
    print("\n── Broken Contract Example ──────────")
    broken = {"id": "not-an-int", "name": 123}  # wrong types
    try:
        jsonschema.validate(broken, USER_SCHEMA)
        print("  ✗ Should have failed")
    except jsonschema.ValidationError as e:
        print(f"  ✓ Caught: {e.message}")


# ─────────────────────────────────────────────
# 3. Check required fields presence
# ─────────────────────────────────────────────
def field_presence():
    print("\n── Required Fields ──────────────────")
    r = requests.get(f"{BASE_URL}/users/1")
    user = r.json()
    required = ["id", "name", "email", "address"]
    missing = [k for k in required if k not in user]
    print(f"  Missing fields: {missing or 'none'}")


# ─────────────────────────────────────────────
# 4. Contract testing in CI
# ─────────────────────────────────────────────
def ci_contracts():
    print("\n── Contracts in CI ──────────────────")
    print("  • Download OpenAPI spec from the API provider")
    print("  • Validate every response against it")
    print("  • Fail the build on schema drift")
    print("  • Use pact.io for consumer/provider matching")


if __name__ == "__main__":
    print("=" * 55)
    print("  CONTRACT TESTING: validate schemas")
    print("=" * 55)
    try:
        import jsonschema  # noqa: F401
        validate_contract()
        broken_contract()
    except ImportError:
        print("  jsonschema not installed — run: pip install jsonschema")
    field_presence()
    ci_contracts()
    print("\nContract testing demos complete.")