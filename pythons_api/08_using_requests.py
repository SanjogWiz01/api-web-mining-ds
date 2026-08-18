"""Practice file: the requests library.

Note: requires `pip install requests`.
This example talks to public JSONPlaceholder endpoints so it actually runs.

Run:  python 08_using_requests.py
"""

import requests


def demo_requests_library() -> None:
    base = "https://jsonplaceholder.typicode.com"

    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})

        print("== GET /posts/1 ==")
        r = session.get(f"{base}/posts/1", timeout=(3, 10))
        print(f"  status={r.status_code}")
        post = r.json()
        print(f"  title: {post['title']}")

        print("== GET with params ==")
        r = session.get(f"{base}/comments", params={"postId": 1}, timeout=(3, 10))
        print(f"  status={r.status_code}, comments returned: {len(r.json())}")

        print("== POST ==")
        r = session.post(f"{base}/posts",
                         json={"title": "Hello", "body": "world", "userId": 1},
                         timeout=(3, 10))
        print(f"  status={r.status_code} (201 = created)")

        print("== PUT ==")
        r = session.put(f"{base}/posts/1",
                        json={"id": 1, "title": "Updated", "userId": 1},
                        timeout=(3, 10))
        print(f"  status={r.status_code}")

        print("== PATCH ==")
        r = session.patch(f"{base}/posts/1", json={"title": "Patched"}, timeout=(3, 10))
        print(f"  status={r.status_code}")

        print("== DELETE ==")
        r = session.delete(f"{base}/posts/1", timeout=(3, 10))
        print(f"  status={r.status_code} (204 = no content)")

        print("== elapsed time ==")
        print(f"  request took {r.elapsed.total_seconds() * 1000:.1f} ms")


if __name__ == "__main__":
    demo_requests_library()
