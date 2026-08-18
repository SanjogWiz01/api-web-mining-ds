"""Practice file: classes, objects, dataclasses, OOP.

Run:  python 05_classes_objects.py
"""

from dataclasses import dataclass, field


class ApiClient:
    """Encapsulate base URL and shared request logic."""

    def __init__(self, base_url: str, api_key: str = ""):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._calls = 0

    def _request(self, method: str, path: str) -> dict:
        self._calls += 1
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        print(f"  [{self._calls}] {method} {self.base_url}{path} headers={headers}")
        return {"status": 200, "ok": True}

    def get(self, path: str) -> dict:
        return self._request("GET", path)

    @property
    def calls(self) -> int:
        """Read-only property."""
        return self._calls


class RetryClient(ApiClient):
    """Inheritance: extends ApiClient with retry logic."""

    def __init__(self, base_url: str, api_key: str = "", max_retries: int = 3):
        super().__init__(base_url, api_key)
        self.max_retries = max_retries

    def _request(self, method: str, path: str) -> dict:
        for attempt in range(self.max_retries):
            result = super()._request(method, path)
            if result["status"] < 500:
                return result
            print(f"    retrying (attempt {attempt + 1})")
        raise RuntimeError("exhausted retries")


@dataclass
class User:
    """Dataclass model - auto __init__, __repr__, __eq__."""
    id: int
    name: str
    email: str = ""
    roles: list[str] = field(default_factory=list)

    def is_admin(self) -> bool:
        return "admin" in self.roles


if __name__ == "__main__":
    print("== plain class ==")
    client = ApiClient("https://api.example.com/v1", api_key="secret")
    print(" ", client.get("/users"))
    print(f"  calls={client.calls}")

    print("== inheritance ==")
    retry_client = RetryClient("https://api.example.com/v1", max_retries=2)
    print(" ", retry_client.get("/users"))

    print("== dataclass ==")
    user = User(id=7, name="Sanjog", email="s@example.com", roles=["admin"])
    print(f"  {user!r}")
    print(f"  is_admin={user.is_admin()}")
