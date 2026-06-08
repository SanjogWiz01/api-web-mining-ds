"""Mine tabular data from HTML pages with pandas."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_URL = "https://www.w3schools.com/html/html_tables.asp"
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs" / "html_tables"


def clean_columns(frame: pd.DataFrame) -> pd.DataFrame:
    cleaned = frame.copy()
    cleaned.columns = [str(column).strip().lower().replace(" ", "_") for column in cleaned.columns]
    return cleaned


def mine_first_table(url: str = DEFAULT_URL) -> pd.DataFrame:
    tables = pd.read_html(url)
    if not tables:
        raise ValueError(f"No HTML tables found at {url}")

    table = clean_columns(tables[0])
    table["source_url"] = url
    table["row_number"] = range(1, len(table) + 1)
    return table


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table = mine_first_table()

    csv_path = OUTPUT_DIR / "first_html_table.csv"
    table.to_csv(csv_path, index=False)

    print(f"Mined table with {len(table)} rows and {len(table.columns)} columns")
    print(f"CSV: {csv_path}")


if __name__ == "__main__":
    main()
