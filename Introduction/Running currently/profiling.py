"""Small dataset profiling helpers for API and scraping projects."""

from __future__ import annotations

import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a compact column-level profile for a DataFrame."""

    rows: list[dict[str, object]] = []
    for column in df.columns:
        series = df[column]
        rows.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "rows": int(len(series)),
                "missing": int(series.isna().sum()),
                "missing_pct": round(float(series.isna().mean() * 100), 2),
                "unique": int(series.nunique(dropna=True)),
                "sample": _sample_value(series),
            }
        )
    return pd.DataFrame(rows)


def _sample_value(series: pd.Series) -> object:
    non_null = series.dropna()
    if non_null.empty:
        return None
    value = non_null.iloc[0]
    if hasattr(value, "item"):
        return value.item()
    return value
