"""Practice file: headers and authentication.

Covers:
  - custom headers (User-Agent, Accept, Authorization)
  - Basic auth
  - API key styles
  - bearer tokens

Run:  python 09_headers_auth.py
"""

import base64
import os

import requests


def demo_headers() -> None:
    print("== custom headers ==")
    r = requests.get(
        "https://jsonplaceholder.typicode.com/posts/1",
        headers={
            "User-Agent": "python-api-course/1.0",
            "Accept": "application/json",
        },
        timeout=(3, 10),
    )
    print(f"  status={r.status_code}")

    print("  response headers:")
    for key in ("content-type", "date", "server"):
        if key in r.headers:
            print(f"    {key}: {r.headers[key]}")


def demo_basic_auth() -> None:
    print("== basic auth (no real secrets, fake endpoint) ==")
    # Real basic auth sends base64("user:pass")
    token = base64.b64encode(b"username:password").decode()
    headers = {"Authorization": f"Basic {token}"}
    r = requests.get("https://httpbin.org/basic-auth/username/password",
                     headers=headers, timeout=(3, 10))
    print(f"  status={r.status_code}, body={r.json()}")


def demo_api_key_and_bearer() -> None:
    print("== api key + bearer ==")
    # Never hardcode secrets in real code - use environment variables.
    api_key = os.environ.get("MY_API_KEY", "demo-key")

    query_params = {"api_key": api_key}   # some APIs take the key in query
    headers = {
        "X-API-Key": api_key,             # others use a custom header
        "Authorization": f"Bearer {api_key}",  # OAuth2/JWT style
    }
    r = requests.get("https://jsonplaceholder.typicode.com/posts/1",
                     params=query_params, headers=headers, timeout=(3, 10))
    print(f"  status={r.status_code}")


def demo_session_auth() -> None:
    print("== session-level auth ==")
    with requests.Session() as session:
        session.headers.update({"User-Agent": "my-app/1.0", "Accept": "application/json"})
        session.auth = ("user", "pass")
        r = session.get("https://httpbin.org/basic-auth/user/pass", timeout=(3, 10))
        print(f"  status={r.status_code}, authenticated={r.json()['authenticated']}")


if __name__ == "__main__":
    demo_headers()
    demo_basic_auth()
    demo_api_key_and_bearer()
    demo_session_auth()
