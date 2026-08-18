"""Practice file: control flow in Python.

Run:  python 03_control_flow.py
"""

import random


def classify_http_status(code: int) -> str:
    """Classify an HTTP status code using if/elif/else."""
    if 200 <= code < 300:
        return "success"
    elif 300 <= code < 400:
        return "redirect"
    elif 400 <= code < 500:
        return "client error"
    elif 500 <= code < 600:
        return "server error"
    else:
        return "unknown"


def check_status_match(code: int) -> str:
    """Classify a status code using Python 3.10+ match statement."""
    match code:
        case 200 | 201 | 204:
            return "OK"
        case 301 | 302:
            return "Redirect"
        case 404:
            return "Not Found"
        case 500:
            return "Server Error"
        case _:
            return f"Unhandled status {code}"


def retry_with_while(attempts: int = 5) -> str:
    """Simulate an API call that succeeds eventually (while loop)."""
    attempt = 0
    while attempt < attempts:
        attempt += 1
        roll = random.randint(1, 6)
        print(f"  attempt {attempt}: rolled {roll}")
        if roll == 6:
            return "SUCCESS"
    raise RuntimeError("gave up after all attempts")


def loop_over_pages(total_pages: int = 3) -> list[str]:
    """Iterate 'pages' with break/continue."""
    collected: list[str] = []
    for page in range(1, total_pages + 1):
        if page == 2:
            print(f"  page {page}: skipping (continue)")
            continue
        if page > total_pages:
            break
        collected.append(f"data-from-page-{page}")
    return collected


def comprehension_demo(items: list[int]) -> tuple[list[int], list[int]]:
    """Demonstrate list comprehensions."""
    doubled = [x * 2 for x in items]
    big_only = [x for x in items if x > 10]
    return doubled, big_only


if __name__ == "__main__":
    print("== if/elif/else ==")
    for code in (200, 301, 404, 500, 600):
        print(f"  {code} -> {classify_http_status(code)}")

    print("== match ==")
    for code in (200, 404, 599):
        print(f"  {code} -> {check_status_match(code)}")

    print("== while/retry ==")
    print("  result:", retry_with_while())

    print("== for/break/continue ==")
    print(" ", loop_over_pages())

    print("== comprehensions ==")
    doubled, big = comprehension_demo([1, 5, 12, 20])
    print(f"  doubled={doubled}, big_only={big}")
