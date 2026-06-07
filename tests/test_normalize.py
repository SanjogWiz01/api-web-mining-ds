from api_web_mining_ds.normalize import flatten_records, normalize_json, select_fields


def test_normalize_json_flattens_nested_records():
    payload = [{"id": 1, "source": {"name": "Demo"}, "metrics": {"views": 10}}]

    df = normalize_json(payload)

    assert list(df.columns) == ["id", "source.name", "metrics.views"]
    assert df.loc[0, "source.name"] == "Demo"


def test_select_fields_extracts_nested_paths_and_missing_values():
    rows = select_fields(
        [{"title": "A", "source": {"name": "News"}}, {"title": "B"}],
        {"title": "title", "source": "source.name"},
    )

    assert rows == [{"title": "A", "source": "News"}, {"title": "B", "source": None}]


def test_flatten_records_accepts_iterables():
    df = flatten_records(record for record in [{"id": 1}, {"id": 2}])

    assert df["id"].tolist() == [1, 2]
