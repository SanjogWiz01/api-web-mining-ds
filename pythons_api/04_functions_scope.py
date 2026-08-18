"""Practice file: functions, arguments, scope, closures, decorators.

Run:  python 04_functions_scope.py
"""

import time


def get_user(user_id: int, include_email: bool = False) -> dict:
    """Positional + keyword args with defaults."""
    user = {"id": user_id, "name": "Sanjog"}
    if include_email:
        user["email"] = "sanjo@example.com"
    return user


def log_request(method: str, url: str, *headers: str, **extra: object) -> None:
    """*args collects extra positional, **kwargs collects keyword extras."""
    print(f"  {method} {url}")
    for h in headers:
        print(f"    header: {h}")
    for k, v in extra.items():
        print(f"    {k}={v}")


double = lambda x: x * 2  # noqa: E731


def make_adder(n: int):
    """Closure: remembers n even after the outer function returns."""
    def adder(x: int) -> int:
        return x + n
    return adder


def timer(func):
    """Decorator: wraps a function to time it."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"  {func.__name__} took {elapsed:.3f} ms")
        return result
    return wrapper


@timer
def slow_fetch():
    time.sleep(0.05)
    return {"data": "ok"}


if __name__ == "__main__":
    print("== defaults ==")
    print(" ", get_user(1))
    print(" ", get_user(1, include_email=True))

    print("== *args / **kwargs ==")
    log_request("GET", "https://api.example.com/users",
                "Accept: application/json",
                retries=3, backoff=0.5)

    print("== lambda ==")
    print(f"  double(21) = {double(21)}")

    print("== closure ==")
    add_five = make_adder(5)
    print(f"  add_five(10) = {add_five(10)}")

    print("== decorator ==")
    print(" ", slow_fetch())
