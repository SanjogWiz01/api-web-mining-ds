"""Basic text mining helpers for collected web datasets."""

from __future__ import annotations

from collections import Counter
import re

import pandas as pd

TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_'-]*")
DEFAULT_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "with",
}


def tokenize(text: str, *, stopwords: set[str] | None = None) -> list[str]:
    ignored = DEFAULT_STOPWORDS if stopwords is None else stopwords
    return [token.lower() for token in TOKEN_PATTERN.findall(text) if token.lower() not in ignored]


def top_terms(texts: list[str] | pd.Series, *, n: int = 10, stopwords: set[str] | None = None) -> pd.DataFrame:
    counter: Counter[str] = Counter()
    for text in texts:
        counter.update(tokenize(str(text), stopwords=stopwords))
    return pd.DataFrame(counter.most_common(n), columns=["term", "count"])


def keyword_counts(texts: list[str] | pd.Series, keywords: list[str]) -> pd.DataFrame:
    normalized_keywords = [keyword.lower() for keyword in keywords]
    rows: list[dict[str, int | str]] = []
    for text in texts:
        lower_text = str(text).lower()
        row: dict[str, int | str] = {"text": str(text)}
        for keyword in normalized_keywords:
            row[keyword] = lower_text.count(keyword)
        rows.append(row)
    return pd.DataFrame(rows)
