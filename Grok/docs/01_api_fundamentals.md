# API Fundamentals for Web Mining

APIs are the safest first choice for web data collection because they usually return structured JSON, publish usage rules, and expose stable query parameters. Use scraping only when an API does not exist or when the HTML page itself is the source of truth.

## Practical Request Checklist

- Set a clear `User-Agent` so the service can identify your client.
- Always use timeouts. A missing timeout can freeze an entire data job.
- Handle status codes before parsing JSON.
- Retry only recoverable failures such as `500`, `502`, `503`, and `504`.
- Treat `429` as a rate-limit signal and slow down.
- Store raw responses before cleaning so you can debug future changes.

## GET Parameters

Most data APIs expose filters as query parameters. For example:

```python
client.get_json(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude": 27.7172,
        "longitude": 85.3240,
        "hourly": "temperature_2m",
    },
)
```

The important habit is to keep parameters as a dictionary instead of manually building URL strings. That avoids encoding bugs and makes pipeline configuration easier to inspect.

## Authentication

Some APIs require an API key, bearer token, OAuth flow, or signed request. Never commit real keys. Put them in `.env`, environment variables, or a secret manager.

```python
headers = {"Authorization": f"Bearer {token}"}
payload = client.get_json("https://api.github.com/user/repos", headers=headers)
```

This v1 course uses unauthenticated examples where possible. Optional keys are listed in `.env.example`.

## Pagination

Large APIs rarely return every record in one response. They usually paginate by page number, offset, cursor, or next URL. The package includes `ApiClient.paginate()` for page-number APIs.

```python
items = client.paginate(
    "https://api.example.com/search",
    page_param="page",
    max_pages=5,
    extract_items=lambda payload: payload["items"],
)
```

In real projects, always log the last successful page or cursor so failed jobs can resume.

## Rate Limits

Rate limits protect services from overload. Common strategies:

- Add small delays between requests.
- Retry `429` after the `Retry-After` header when the API provides it.
- Cache repeated requests.
- Prefer bulk endpoints over thousands of single-record calls.

The retry helper in `ApiClient` intentionally stays conservative. Production jobs should also add persistent checkpoints and structured logging.
