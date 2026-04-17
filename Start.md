import requests
import pandas as pd
import time
import os

# ==============================
# CONFIGURATION
# ==============================

API_KEY = "YOUR_API_KEY"   # Replace with your API key
BASE_URL = "https://newsapi.org/v2/top-headlines"

PARAMS = {
    "country": "us",
    "category": "technology",
    "pageSize": 20,
    "apiKey": API_KEY
}

OUTPUT_DIR = "data"
RAW_FILE = os.path.join(OUTPUT_DIR, "raw.json")
CLEAN_FILE = os.path.join(OUTPUT_DIR, "cleaned.csv")

# ==============================
# CREATE DATA DIRECTORY
# ==============================

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==============================
# FETCH DATA FROM API
# ==============================

def fetch_data():
    try:
        response = requests.get(BASE_URL, params=PARAMS, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Save raw JSON
        with open(RAW_FILE, "w") as f:
            import json
            json.dump(data, f, indent=4)

        print("✅ Data fetched successfully")
        return data

    except requests.exceptions.RequestException as e:
        print("❌ API Request Failed:", e)
        return None

# ==============================
# CLEAN DATA
# ==============================

def clean_data(data):
    if not data or "articles" not in data:
        print("❌ No data to clean")
        return None

    articles = data["articles"]

    cleaned = []
    for article in articles:
        cleaned.append({
            "title": article.get("title"),
            "author": article.get("author"),
            "source": article.get("source", {}).get("name"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url")
        })

    df = pd.DataFrame(cleaned)

    # Drop missing values
    df.dropna(inplace=True)

    # Save cleaned data
    df.to_csv(CLEAN_FILE, index=False)

    print("✅ Data cleaned and saved")
    return df

# ==============================
# ANALYSIS
# ==============================

def analyze_data(df):
    if df is None:
        return

    print("\n📊 Basic Analysis:")

    print("\nTop Authors:")
    print(df["author"].value_counts().head())

    print("\nTop Sources:")
    print(df["source"].value_counts().head())

# ==============================
# VISUALIZATION
# ==============================

def visualize(df):
    if df is None:
        return

    import matplotlib.pyplot as plt

    source_counts = df["source"].value_counts().head(5)

    plt.figure()
    source_counts.plot(kind="bar")
    plt.title("Top News Sources")
    plt.xlabel("Source")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN PIPELINE
# ==============================

def main():
    print("🚀 Starting Web Mining Pipeline...\n")

    data = fetch_data()

    # Avoid hitting rate limits
    time.sleep(1)

    df = clean_data(data)

    analyze_data(df)

    visualize(df)

    print("\n✅ Pipeline Completed Successfully")

# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()      