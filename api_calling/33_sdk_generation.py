"""
📘 TOPIC 33: SDK Generation — Turn Specs Into Clients
====================================================
Instead of writing HTTP calls by hand, generate a typed client
(SDK) from the API's OpenAPI specification.

Popular generators:
  OpenAPI Generator (openapi-generator)
  swagger-codegen
  autorest (Azure)
  openapi-python-client

This keeps field names, types, and endpoints in sync with the API.
"""

import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


# ─────────────────────────────────────────────
# 1. Hand-rolled client (what we've been doing)
# ─────────────────────────────────────────────
class HandRolledClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_post(self, post_id):
        return requests.get(f"{self.base_url}/posts/{post_id}").json()

    def get_user(self, user_id):
        return requests.get(f"{self.base_url}/users/{user_id}").json()


def hand_rolled():
    print("\n── Hand-Rolled Client ───────────────")
    client = HandRolledClient(BASE_URL)
    post = client.get_post(1)
    print(f"  post.title: {post['title'][:45]}")


# ─────────────────────────────────────────────
# 2. Generated SDK shape (illustration)
# ─────────────────────────────────────────────
def generated_sdk_shape():
    print("\n── Generated SDK Shape ──────────────")
    code = '''
# Generated from openapi.json by openapi-python-client
from myapi_client import Client
from myapi_client.api.posts import get_post

client = Client(base_url="https://api.example.com", token="...")

with client as c:
    post = get_post.sync(client=c, post_id=1)
    print(post.title)   # typed, validated, no manual HTTP
'''
    print(code)


# ─────────────────────────────────────────────
# 3. OpenAPI spec → SDK flow
# ─────────────────────────────────────────────
def spec_to_sdk():
    print("\n── OpenAPI → SDK Pipeline ───────────")
    steps = [
        "1. Provider publishes openapi.json (machine-readable contract)",
        "2. `openapi-generator generate -i openapi.json -g python -o ./client`",
        "3. SDK ships typed models, endpoints, and error types",
        "4. Provider updates spec → regenerate → everything stays in sync",
    ]
    for s in steps:
        print(f"  {s}")


# ─────────────────────────────────────────────
# 4. Pros & cons
# ─────────────────────────────────────────────
def pros_cons():
    print("\n── Pros & Cons ──────────────────────")
    print("  + No manual URL/JSON plumbing, types checked at compile time")
    print("  + Auto-updates when the API spec changes")
    print("  + Consistent across languages")
    print("  - Generated code can be large/verbose")
    print("  - Adds a build step and dependency")


if __name__ == "__main__":
    print("=" * 55)
    print("  SDK GENERATION: from spec to client")
    print("=" * 55)
    hand_rolled()
    generated_sdk_shape()
    spec_to_sdk()
    pros_cons()
    print("\nSDK demos complete.")