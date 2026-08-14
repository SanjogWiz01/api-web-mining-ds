"""
📘 TOPIC 7: Data Format — JSON is the Standard
===============================================
JSON (JavaScript Object Notation) is the universal data format for REST APIs.
Key operations:
  - Serialize Python dict  → JSON string  (json.dumps)
  - Deserialize JSON string → Python dict  (json.loads)
  - Send JSON in request   → requests.post(json=payload)
  - Receive JSON response  → response.json()

Validation is critical: always check field types before using them!
"""

import requests
import json
from typing import Any


BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# JSON Serialization / Deserialization
# ─────────────────────────────────────────────
def json_basics():
    print("\n── JSON Encode / Decode ─────────────")
    data = {
        "name": "Alice",
        "age": 30,
        "active": True,
        "scores": [95, 87, 92],
        "address": {"city": "Kathmandu", "zip": "44600"}
    }
    # Python dict → JSON string
    json_str = json.dumps(data, indent=2)
    print(f"Serialized JSON:\n{json_str}")

    # JSON string → Python dict
    parsed = json.loads(json_str)
    print(f"\nParsed back: {parsed['name']}, Age: {parsed['age']}")
    print(f"Nested city: {parsed['address']['city']}")
    print(f"Score avg  : {sum(parsed['scores']) / len(parsed['scores']):.1f}")


# ─────────────────────────────────────────────
# Parsing & Validating API Response JSON
# ─────────────────────────────────────────────
def parse_and_validate():
    print("\n── Parse & Validate API Response ───")
    r = requests.get(f"{BASE_URL}/users/1")
    data = r.json()

    # Safely access nested fields with .get()
    name    = data.get("name", "Unknown")
    email   = data.get("email", "No email")
    city    = data.get("address", {}).get("city", "No city")
    company = data.get("company", {}).get("name", "No company")
    lat     = data.get("address", {}).get("geo", {}).get("lat", None)

    print(f"  Name   : {name}")
    print(f"  Email  : {email}")
    print(f"  City   : {city}")
    print(f"  Company: {company}")
    print(f"  Lat    : {lat} (type: {type(lat).__name__})")

    # Type validation
    print("\n── Type Validation ──────────────────")
    validations = {
        "id":    (int, data.get("id")),
        "name":  (str, data.get("name")),
        "email": (str, data.get("email")),
    }
    for field, (expected_type, value) in validations.items():
        is_valid = isinstance(value, expected_type)
        print(f"  {field:<8} | expected={expected_type.__name__:<5} | "
              f"got={type(value).__name__:<5} | valid={is_valid}")


# ─────────────────────────────────────────────
# Pretty Print & Save JSON to File
# ─────────────────────────────────────────────
def save_json_to_file():
    print("\n── Save API JSON Response to File ───")
    r = requests.get(f"{BASE_URL}/posts", params={"_limit": 5})
    posts = r.json()

    output_file = "api_response_sample.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"  Saved {len(posts)} posts to '{output_file}'")
    print(f"  Keys in each post: {list(posts[0].keys())}")


# ─────────────────────────────────────────────
# Sending JSON in Request Body
# ─────────────────────────────────────────────
def send_json_body():
    print("\n── Sending JSON in POST Body ────────")
    payload = {
        "title": "JSON Data Format Tutorial",
        "body": "JSON is human-readable and machine-parseable",
        "userId": 7,
        "tags": ["python", "api", "json"],
        "meta": {"priority": "high", "draft": False}
    }
    # Tip: use json= not data= to auto-set Content-Type: application/json
    r = requests.post(f"{BASE_URL}/posts", json=payload)
    print(f"  Status       : {r.status_code}")
    print(f"  Content-Type : {r.request.headers.get('Content-Type')}")
    response_data = r.json()
    print(f"  Created ID   : {response_data.get('id')}")
    print(f"  Title        : {response_data.get('title')}")


if __name__ == "__main__":
    print("=" * 55)
    print("  DATA FORMAT: JSON Parsing, Validation & Serialization")
    print("=" * 55)
    json_basics()
    parse_and_validate()
    send_json_body()
    save_json_to_file()
    print("\nJSON data format demos complete.")
