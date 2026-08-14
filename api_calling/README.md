# API Calling — 10 Fundamental Concepts

A structured Python learning series covering the 10 essential concepts
every developer must know before working with REST APIs.

## Topics

| File | Topic | Key Concepts |
|------|-------|--------------|
| `01_http_basics.py` | HTTP Basics | GET, POST, PUT, DELETE |
| `02_authentication.py` | Authentication | API Keys, Bearer Token, Basic Auth |
| `03_endpoints.py` | Endpoints | Base URL, Path Variables, Query Params |
| `04_request_headers.py` | Request Headers | Content-Type, Authorization, Accept |
| `05_error_handling.py` | Error Handling | 200/400/401/404/500, raise_for_status |
| `06_rate_limits.py` | Rate Limits | Exponential Backoff, Throttling |
| `07_data_format_json.py` | Data Format | JSON encode/decode, validation |
| `08_security.py` | Security | env vars, .env, HTTPS, safe logging |
| `09_documentation.py` | Documentation | API docs, schema validation |
| `10_testing_tools.py` | Testing Tools | curl, Postman, automated tests |

## Setup

```bash
pip install requests
```

## Usage

```bash
# Run all 10 topics
python main.py

# Run a specific topic
python main.py 3

# Run selected topics
python main.py 1 5 10

# Run any file directly
python 01_http_basics.py
```

## Test API Used

All examples use [JSONPlaceholder](https://jsonplaceholder.typicode.com/) — a free, public fake REST API for testing and prototyping. No API key required.

## Security Note

> Never commit API keys to version control. Always use environment variables or `.env` files (added to `.gitignore`).
