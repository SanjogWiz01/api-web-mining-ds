# HTTP and the requests library

## The HTTP protocol in one page

Every web API call is a `METHOD + URL + HEADERS + BODY`.

### Methods (verbs)

| Method | Purpose            | Typical API usage          |
|--------|--------------------|----------------------------|
| GET    | Read               | fetch a resource           |
| POST   | Create             | create a resource          |
| PUT    | Replace            | full update                |
| PATCH  | Partial update     | update some fields         |
| DELETE | Remove             | delete a resource          |

### Status codes (remember the ranges)

```
2xx  Success        200 OK, 201 Created, 204 No Content
3xx  Redirection    301, 302, 304 Not Modified
4xx  Client error   400 Bad Request, 401 Unauthorized, 403 Forbidden,
                    404 Not Found, 429 Too Many Requests
5xx  Server error   500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable
```

## The `requests` library

```python
import requests

r = requests.get("https://api.example.com/v1/users")
r.status_code        # 200
r.headers            # case-insensitive dict
r.json()             # parsed JSON (or raise JSONDecodeError)
r.text               # raw string
r.content            # raw bytes
```

Every `requests` call returns a `Response` object with:

- `.status_code`
- `.headers`
- `.json()`
- `.raise_for_status()` — raises `requests.HTTPError` for 4xx/5xx
- `.elapsed` — how long the request took

## Sessions (do this, not bare calls)

```python
with requests.Session() as session:
    session.headers.update({"User-Agent": "my-app/1.0"})
    session.auth = ("user", "pass")
    r = session.get(url)   # session keeps cookies, pools connections
```

Benefits: connection pooling, persistent headers/cookies, retries config.

## Common request options

```python
requests.get(
    url,
    params={"page": 1, "limit": 20},   # query string
    headers={"Accept": "application/json"},
    auth=("user", "password"),          # Basic auth
    timeout=(3.05, 10),                 # (connect, read)
    proxies={"https": "http://proxy:8080"},
    verify=False,                       # NEVER in production
)
```

Always set a `timeout` — otherwise your program can hang forever.

## Minimal but robust request helper

```python
def safe_get(session, url, **kwargs):
    kwargs.setdefault("timeout", (3, 10))
    r = session.get(url, **kwargs)
    r.raise_for_status()
    return r.json()
```

Practice in `08_using_requests.py` and the following files.
