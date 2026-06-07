"""Fetch posts from JSONPlaceholder and normalize them into a DataFrame."""

from api_web_mining_ds import ApiClient, ApiClientConfig, normalize_json, profile_dataframe


def main() -> None:
    client = ApiClient(ApiClientConfig(retries=2, backoff_seconds=0.2))
    posts = client.get_json("https://jsonplaceholder.typicode.com/posts")

    df = normalize_json(posts)
    df = df.rename(columns={"userId": "user_id"})

    print(df[["user_id", "id", "title"]].head())
    print("\nProfile:")
    print(profile_dataframe(df).head())


if __name__ == "__main__":
    main()
