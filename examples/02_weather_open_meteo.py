"""Collect a small weather dataset from Open-Meteo's public API."""

from api_web_mining_ds import ApiClient, ApiClientConfig, normalize_json


def main() -> None:
    client = ApiClient(ApiClientConfig(retries=2, backoff_seconds=0.2))
    payload = client.get_json(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 27.7172,
            "longitude": 85.3240,
            "hourly": "temperature_2m,relative_humidity_2m",
            "forecast_days": 1,
        },
    )

    hourly = payload["hourly"]
    df = normalize_json(
        [
            {
                "time": time,
                "temperature_2m": hourly["temperature_2m"][index],
                "relative_humidity_2m": hourly["relative_humidity_2m"][index],
            }
            for index, time in enumerate(hourly["time"])
        ]
    )
    print(df.head())


if __name__ == "__main__":
    main()
