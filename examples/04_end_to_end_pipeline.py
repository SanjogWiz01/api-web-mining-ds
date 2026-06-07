"""Run the complete collect-clean-store-report mini project."""

from pathlib import Path

from api_web_mining_ds import ApiClient, ApiClientConfig
from api_web_mining_ds.pipeline import collect_posts_project


def main() -> None:
    client = ApiClient(ApiClientConfig(retries=2, backoff_seconds=0.2))
    outputs = collect_posts_project(client=client, output_dir=Path("data/jsonplaceholder_posts"))

    print("Generated project outputs:")
    print(f"- Raw JSON: {outputs.raw_json}")
    print(f"- Clean CSV: {outputs.clean_csv}")
    print(f"- SQLite DB: {outputs.sqlite_db}")
    print(f"- Profile CSV: {outputs.profile_csv}")
    print(f"- Terms CSV: {outputs.terms_csv}")


if __name__ == "__main__":
    main()
