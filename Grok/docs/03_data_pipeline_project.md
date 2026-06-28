# End-to-End Data Pipeline Project

The mini project in `examples/04_end_to_end_pipeline.py` demonstrates the full workflow:

1. Collect raw API data from JSONPlaceholder.
2. Save the raw JSON response.
3. Normalize the JSON into a DataFrame.
4. Clean and enrich fields.
5. Save CSV and SQLite outputs.
6. Generate a data profile.
7. Mine frequent title terms.

## Why Save Raw Data?

Raw data is your audit trail. If a cleaning rule looks wrong later, you can reproduce the transformation without calling the remote source again.

## Cleaning Rules in the Project

The project keeps `user_id`, `id`, `title`, and `body`, drops incomplete rows, and adds:

- `title_length`
- `body_word_count`

Those features are simple, but they demonstrate how practical data mining starts: collect clean records, add measurable fields, and save outputs for downstream analysis.

## Storage Choices

- JSON preserves the original response.
- CSV is easy to inspect and share.
- SQLite is useful for repeatable local analysis and joins.

For larger real-life projects, move from SQLite to PostgreSQL, DuckDB, or a cloud warehouse depending on query size and collaboration needs.

## Acceptance Criteria for Your Own Project

- The pipeline can run from one command.
- It stores raw and cleaned data separately.
- It can be tested without live web calls.
- It has a clear rate-limit strategy.
- It produces at least one useful analysis artifact.
