"""
📘 TOPIC 38: Data Normalization & Validation
===========================================
Raw API responses are messy: extra fields, inconsistent types,
missing values. Normalize and validate before analysis.

Steps:
  coerce types → strip whitespace → default missing values → validate
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Raw response inspection
# ─────────────────────────────────────────────
def raw_inspection():
    print("\n── Raw Response ─────────────────────")
    r = requests.get(f"{BASE_URL}/users/1")
    raw = r.json()
    print(json.dumps(raw, indent=2)[:400])
    return raw


# ─────────────────────────────────────────────
# 2. Normalization function
# ─────────────────────────────────────────────
def normalize_user(user: dict) -> dict:
    return {
        "id": int(user.get("id", 0)),
        "name": (user.get("name") or "").strip().title(),
        "email": (user.get("email") or "").strip().lower(),
        "username": (user.get("username") or "").strip(),
        "city": ((user.get("address") or {}).get("city") or "unknown").strip(),
        "company": ((user.get("company") or {}).get("name") or "unknown").strip(),
    }


def run_normalize():
    print("\n── Normalized ───────────────────────")
    user = requests.get(f"{BASE_URL}/users/1").json()
    clean = normalize_user(user)
    print(json.dumps(clean, indent=2))


# ─────────────────────────────────────────────
# 3. Batch normalization of a list
# ─────────────────────────────────────────────
def batch_normalize():
    print("\n── Batch Normalize ──────────────────")
    r = requests.get(f"{BASE_URL}/users", params={"_limit": 5})
    clean_users = [normalize_user(u) for u in r.json()]
    print(f"  Normalized {len(clean_users)} users")
    for u in clean_users:
        print(f"    {u['id']}: {u['name']} <{u['email']}> — {u['city']}")


# ─────────────────────────────────────────────
# 4. Validation pass
# ─────────────────────────────────────────────
def validation():
    print("\n── Validation Pass ──────────────────")
    user = normalize_user(requests.get(f"{BASE_URL}/users/1").json())
    checks = [
        ("has id", isinstance(user["id"], int)),
        ("has email", "@" in user["email"]),
        ("has name", len(user["name"]) > 0),
    ]
    for label, ok in checks:
        print(f"  {'✓' if ok else '✗'} {label}")
    if all(ok for _, ok in checks):
        print("  → Record valid, ready for storage")


if __name__ == "__main__":
    print("=" * 55)
    print("  NORMALIZATION: clean API data")
    print("=" * 55)
    raw_inspection()
    run_normalize()
    batch_normalize()
    validation()
    print("\nNormalization demos complete.")