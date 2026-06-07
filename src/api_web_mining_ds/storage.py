"""Storage helpers for repeatable data collection projects."""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
from typing import Any

import pandas as pd


def save_json(payload: Any, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_path


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_csv(df: pd.DataFrame, path: str | Path) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def save_sqlite(df: pd.DataFrame, db_path: str | Path, *, table_name: str, if_exists: str = "replace") -> Path:
    output_path = Path(db_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(output_path) as connection:
        df.to_sql(table_name, connection, if_exists=if_exists, index=False)
    return output_path


def load_sqlite_table(db_path: str | Path, *, table_name: str) -> pd.DataFrame:
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
