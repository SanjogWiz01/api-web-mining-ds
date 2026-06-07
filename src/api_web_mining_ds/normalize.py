"""JSON normalization helpers for turning API payloads into tables."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import pandas as pd


def normalize_json(
    payload: Any,
    *,
    record_path: str | list[str] | None = None,
    meta: list[str] | None = None,
    separator: str = ".",
) -> pd.DataFrame:
    """Normalize list/dict JSON payloads into a DataFrame."""

    if record_path is None:
        if isinstance(payload, dict):
            records = payload.get("items") or payload.get("results") or payload.get("data") or payload
        else:
            records = payload
        return pd.json_normalize(records, sep=separator)

    return pd.json_normalize(payload, record_path=record_path, meta=meta, sep=separator)


def flatten_records(records: Iterable[dict[str, Any]], *, separator: str = ".") -> pd.DataFrame:
    """Flatten an iterable of dictionaries into a tabular DataFrame."""

    return pd.json_normalize(list(records), sep=separator)


def select_fields(records: Iterable[dict[str, Any]], field_map: dict[str, str]) -> list[dict[str, Any]]:
    """Extract nested fields from records using dotted paths."""

    selected: list[dict[str, Any]] = []
    for record in records:
        row: dict[str, Any] = {}
        for output_name, dotted_path in field_map.items():
            row[output_name] = _get_path(record, dotted_path)
        selected.append(row)
    return selected


def _get_path(record: dict[str, Any], dotted_path: str) -> Any:
    current: Any = record
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current
