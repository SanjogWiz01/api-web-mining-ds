"""Practice file: testing an API client with pytest.

Run:
    pip install pytest responses
    pytest 24_api_tests.py -v
"""

import responses
import pytest

import requests


class ApiError(Exception):
    pass


class ApiClient:
    """Small client used to demonstrate testing (mirrors file 19)."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_user(self, user_id: int) -> dict:
        r = requests.get(f"{self.base_url}/users/{user_id}", timeout=5)
        if r.status_code == 404:
            raise ApiError("User not found")
        r.raise_for_status()
        return r.json()

    def list_posts(self, page: int = 1, limit: int = 10) -> list[dict]:
        r = requests.get(f"{self.base_url}/posts", params={"page": page, "limit": limit}, timeout=5)
        r.raise_for_status()
        return r.json()


@pytest.fixture
def client():
    return ApiClient("https://api.example.com/v1")


@responses.activate
def test_get_user_ok(client):
    responses.add(
        responses.GET, "https://api.example.com/v1/users/1",
        json={"id": 1, "name": "Sanjog"}, status=200,
    )
    user = client.get_user(1)
    assert user["name"] == "Sanjog"


@responses.activate
def test_get_user_missing_raises(client):
    responses.add(
        responses.GET, "https://api.example.com/v1/users/1", status=404,
    )
    with pytest.raises(ApiError):
        client.get_user(1)


@responses.activate
def test_get_user_server_error_raises(client):
    responses.add(
        responses.GET, "https://api.example.com/v1/users/1", status=500,
    )
    with pytest.raises(requests.HTTPError):
        client.get_user(1)


@responses.activate
def test_list_posts_passes_params(client):
    def request_callback(request):
        assert request.params["page"] == "2"
        assert request.params["limit"] == "5"
        return (200, {}, '[{"id": 1}]')

    responses.add_callback(
        responses.GET, "https://api.example.com/v1/posts",
        callback=request_callback,
    )
    posts = client.list_posts(page=2, limit=5)
    assert posts == [{"id": 1}]


@responses.activate
def test_list_posts_empty(client):
    responses.add(
        responses.GET, "https://api.example.com/v1/posts",
        json=[], status=200,
    )
    assert client.list_posts() == []


# ------------------------------------------------------------ pure functions
def parse_page_header(link_header: str) -> dict[str, str]:
    """Parse an RFC 5988 Link header into {rel: url}."""
    result = {}
    for part in link_header.split(","):
        if ";" not in part:
            continue
        url, _, params = part.partition(";")
        rel = "next"
        for piece in params.split(";"):
            if piece.strip().startswith("rel="):
                rel = piece.strip()[5:].strip('"')
        result[rel] = url.strip().strip("<>")
    return result


def test_parse_link_header():
    header = '<https://api.example.com/posts?page=2>; rel="next", <https://api.example.com/posts?page=0>; rel="prev"'
    parsed = parse_page_header(header)
    assert parsed["next"] == "https://api.example.com/posts?page=2"
    assert parsed["prev"] == "https://api.example.com/posts?page=0"
