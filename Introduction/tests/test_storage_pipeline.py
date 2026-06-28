import pandas as pd

from Grok.api_web_mining_ds.pipeline import clean_news_articles, collect_posts_project
from Grok.api_web_mining_ds.storage import load_sqlite_table, read_json, save_csv, save_json, save_sqlite


class FakeClient:
    def get_json(self, url):
        assert "jsonplaceholder" in url
        return [
            {"userId": 1, "id": 1, "title": "API mining basics", "body": "Collect clean data."},
            {"userId": 1, "id": 2, "title": "Web data project", "body": "Store and analyze records."},
        ]


def test_storage_round_trip(tmp_path):
    payload = {"items": [{"id": 1}]}
    df = pd.DataFrame([{"id": 1, "name": "Ada"}])

    json_path = save_json(payload, tmp_path / "raw" / "payload.json")
    csv_path = save_csv(df, tmp_path / "clean" / "items.csv")
    db_path = save_sqlite(df, tmp_path / "db" / "items.sqlite", table_name="items")

    assert read_json(json_path) == payload
    assert pd.read_csv(csv_path).to_dict("records") == [{"id": 1, "name": "Ada"}]
    assert load_sqlite_table(db_path, table_name="items").to_dict("records") == [{"id": 1, "name": "Ada"}]


def test_collect_posts_project_creates_all_outputs(tmp_path):
    outputs = collect_posts_project(client=FakeClient(), output_dir=tmp_path)

    assert outputs.raw_json.exists()
    assert outputs.clean_csv.exists()
    assert outputs.sqlite_db.exists()
    assert outputs.profile_csv.exists()
    assert outputs.terms_csv.exists()

    clean_df = pd.read_csv(outputs.clean_csv)
    assert clean_df["body_word_count"].tolist() == [3, 4]


def test_clean_news_articles_keeps_required_records():
    articles = [
        {
            "title": "Useful API",
            "author": "Sanjog",
            "source": {"name": "Demo News"},
            "publishedAt": "2026-06-07T00:00:00Z",
            "url": "https://example.com/a",
        },
        {"title": None, "source": {"name": "Broken"}, "url": "https://example.com/b"},
    ]

    df = clean_news_articles(articles)

    assert df.to_dict("records") == [
        {
            "title": "Useful API",
            "author": "Sanjog",
            "source": "Demo News",
            "published_at": "2026-06-07T00:00:00Z",
            "url": "https://example.com/a",
        }
    ]
