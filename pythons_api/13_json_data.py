"""Practice file: JSON - the lingua franca of APIs.

Covers serialization, deserialization, schema validation, and safe parsing.

Run:  python 13_json_data.py
"""

import json
from dataclasses import asdict, dataclass
from typing import Any


def demo_basics() -> None:
    print("== json.dumps / json.loads ==")
    payload = {"name": "Sanjog", "tags": ["api", "python"], "ok": True}
    text = json.dumps(payload, indent=2)
    print(text)
    back = json.loads(text)
    assert back == payload
    print("  round-trip OK")


def demo_types() -> None:
    print("== JSON <-> Python type mapping ==")
    mapping = {
        "object": dict, "array": list, "string": str,
        "number": (int, float), "boolean": bool, "null": type(None),
    }
    print(f"  {mapping}")


@dataclass
class Post:
    id: int
    title: str
    body: str = ""
    tags: list[str] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Post":
        return cls(
            id=int(data.get("id", 0)),
            title=str(data.get("title", "")),
            body=str(data.get("body", "")),
            tags=[str(t) for t in data.get("tags", [])] if data.get("tags") else None,
        )


def safe_parse(text: str) -> dict[str, Any] | None:
    """Never let a bad body crash your caller."""
    try:
        data = json.loads(text)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        return None


def demo_dataclass_mapping() -> None:
    print("== dict -> dataclass ==")
    raw = {"id": 3, "title": "Hello", "body": "world", "tags": ["a", "b"]}
    post = Post.from_dict(raw)
    print(f"  {post}")

    print("== dataclass -> json ==")
    print(f"  {json.dumps(asdict(post), indent=2)}")


def demo_validate() -> None:
    print("== minimal schema validation ==")
    data = safe_parse('{"id": 1, "title": "x", "tags": []}')

    required = {"id": int, "title": str}
    errors = [
        f"{field} missing or wrong type"
        for field, expected in required.items()
        if not isinstance(data.get(field), expected)
    ]
    print(f"  errors={errors or 'none'}")


def demo_real_api() -> None:
    print("== real API JSON ==")
    import requests

    r = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=(3, 10))
    post = Post.from_dict(r.json())
    print(f"  id={post.id}, title={post.title[:25]}...")
    print(f"  extra key user_id was dropped safely by from_dict")


if __name__ == "__main__":
    demo_basics()
    demo_types()
    demo_dataclass_mapping()
    demo_validate()
    demo_real_api()
