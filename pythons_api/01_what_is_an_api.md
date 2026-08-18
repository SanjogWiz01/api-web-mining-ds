# What is an API?

An **Application Programming Interface (API)** is a contract that lets one piece
of software talk to another. In the context of web APIs (REST, GraphQL, etc.),
it is a set of HTTP endpoints that expose data and actions over the network.

## Why Python for APIs?

- Batteries included: `urllib`, `http.client`, `json`.
- Great third-party ecosystem: `requests`, `httpx`, `aiohttp`.
- Excellent frameworks for *building* APIs: Flask, FastAPI, Django REST Framework.
- Clear, readable syntax that mirrors API documentation.

## The Big Picture

```
[Client app]  --HTTP-->  [Web API]  --logic-->  [Database / Services]
     ^                        |
     |--------JSON/XML--------|
```

The client sends a **request**; the API returns a **response**.

## Core concepts to learn in this folder

| Topic | What you will learn |
|-------|---------------------|
| HTTP | Methods, status codes, headers, body |
| Requests | Calling APIs with `requests` and `httpx` |
| Auth | API keys, Basic auth, OAuth2, JWT |
| Data | JSON, XML, serialization |
| Reliability | Retries, backoff, rate limiting, caching |
| Design | RESTful resource design, versioning |
| Building | Flask and FastAPI applications |
| Production | Monitoring, testing, deployment, async |

## Analogy

A restaurant:
- The **menu** is the API documentation (what you can order).
- The **waiter** is the API endpoint (takes your order, brings food).
- The **kitchen** is the server logic/database.
- The **food** is the JSON response.

Work through the numbered files in this folder in order. Notes (`.md`) give you
theory, practice files (`.py`) give you runnable examples, and the last files are
production-grade API implementations.
