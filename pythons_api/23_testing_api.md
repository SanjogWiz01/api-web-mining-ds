# Testing APIs

An API is only trustworthy if it is tested. This page covers the two sides:
testing *against* an API (clients) and testing *an* API (servers).

## 1. What to test

- Status codes for happy paths and error paths.
- Response schema / shape (keys, types).
- Validation rules (bad input -> 400/422).
- Auth: no token -> 401, bad token -> 403.
- Pagination: page/limit math.
- Idempotency and retries.
- Rate limiting and concurrency.

## 2. Tools in the Python world

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner + assertions |
| `requests`/`httpx` | Real HTTP calls in tests |
| `responses` / `respx` | Mock HTTP responses for clients |
| `pytest-mock` | Monkeypatch anything |
| FastAPI `TestClient` | In-process testing of FastAPI apps |
| `pytest-asyncio` | Async test support |
| `tox` / `nox` | Run tests in multiple environments |

## 3. Testing a client (mock the network)

Never hit the real API in CI. Mock it:

```python
import responses
import pytest
from my_client import ApiClient

@responses.activate
def test_get_user_ok():
    responses.add(
        responses.GET, "https://api.example.com/v1/users/1",
        json={"id": 1, "name": "Sanjog"}, status=200,
    )
    client = ApiClient("https://api.example.com/v1")
    assert client.get_user(1)["name"] == "Sanjog"

@responses.activate
def test_get_user_missing():
    responses.add(responses.GET, "https://api.example.com/v1/users/1", status=404)
    client = ApiClient("https://api.example.com/v1")
    with pytest.raises(ApiError):
        client.get_user(1)
```

## 4. Testing a FastAPI app in-process

```python
from fastapi.testclient import TestClient
from my_app import app

client = TestClient(app)

def test_list_items():
    r = client.get("/items?page=1&limit=5")
    assert r.status_code == 200
    assert "data" in r.json()
    assert r.json()["meta"]["total"] >= 0

def test_create_item_validation():
    r = client.post("/items", json={"name": ""})
    assert r.status_code == 422          # Pydantic rejects empty name

def test_health():
    r = client.get("/health")
    assert r.json() == {"status": "ok"}
```

## 5. Contract / schema testing

Use `jsonschema` to validate the response shape:

```python
import jsonschema

SCHEMA = {
    "type": "object",
    "required": ["data", "meta"],
    "properties": {
        "data": {"type": "array"},
        "meta": {"type": "object"},
    },
}

def test_posts_shape():
    r = client.get("/posts")
    jsonschema.validate(r.json(), SCHEMA)
```

## 6. Practical tips

- Tests must be deterministic: freeze time, mock randomness, control the DB.
- Use factories/seed data instead of depending on state order.
- Run tests in CI on every push.
- Aim for coverage of the important paths, not 100% for its own sake.
- Test the contract, not the implementation details.

See `24_api_tests.py` for a full runnable example.
