# Exceptions and Error Handling in Python

Robust API code must anticipate failure. Python's `try/except` is your primary
tool.

## The exception hierarchy (relevant parts)

```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── ArithmeticError
      ├── OSError            (ConnectionError, TimeoutError...)
      ├── ValueError
      ├── KeyError
      ├── TypeError
      └── (your custom ones)
```

Catch `Exception`, not `BaseException`, unless you really mean it.

## Basic pattern

```python
try:
    r = requests.get(url, timeout=5)
    r.raise_for_status()
except requests.Timeout:
    handle_timeout()
except requests.HTTPError:
    handle_http(r.status_code)
except requests.RequestException:
    handle_network()
else:
    data = r.json()      # only runs if no exception
finally:
    close_everything()
```

- `else` runs when no exception occurred.
- `finally` always runs (cleanup).

## raise vs raise from

```python
raise ApiError("request failed") from exc   # chaining - keeps context
```

## Custom exceptions

```python
class ApiError(Exception):
    pass

class RateLimitedError(ApiError):
    def __init__(self, retry_after: float):
        super().__init__(f"rate limited, retry after {retry_after}s")
        self.retry_after = retry_after
```

Custom exceptions let callers handle API failures precisely instead of checking
strings.

## EAFP vs LBYL

- **EAFP** (Easier to Ask Forgiveness than Permission) — Pythonic: try it and catch.
- **LBYL** (Look Before You Leap): check with `if` first.

```python
# EAFP
try:
    data["user"]["email"]
except (KeyError, TypeError):
    email = ""

# LBYL
email = data.get("user", {}).get("email", "")
```

For API response parsing, prefer defensive `.get()` + EAFP for the rest.

## Never swallow errors silently

```python
try:
    r = api.get(url)
except ApiError:
    pass          # BAD - hides failures
```

Log, raise, or return a well-defined fallback instead.
