"""Reusable utilities for practical API and web mining workflows."""

from .http_client import ApiClient, ApiClientConfig, ApiError, RateLimitError
from .async_client import AsyncApiConfig, fetch_json_many
from .normalize import flatten_records, normalize_json, select_fields
from .profiling import profile_dataframe
from .scraper import HtmlScraper, RobotsPolicy
from .storage import read_json, save_csv, save_json, save_sqlite
from .text_mining import keyword_counts, top_terms

__all__ = [
    "ApiClient",
    "ApiClientConfig",
    "AsyncApiConfig",
    "ApiError",
    "RateLimitError",
    "fetch_json_many",
    "flatten_records",
    "normalize_json",
    "select_fields",
    "profile_dataframe",
    "HtmlScraper",
    "RobotsPolicy",
    "read_json",
    "save_csv",
    "save_json",
    "save_sqlite",
    "keyword_counts",
    "top_terms",
]
