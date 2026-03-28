import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"
data = requests.get(url).json()

df = pd.DataFrame(data)

# Basic data mining
print("Total Posts:", len(df))

# Count posts per user
user_counts = df['userId'].value_counts()
print("\nPosts per user:\n", user_counts)

# Find user with max posts
top_user = user_counts.idxmax()
print("\nUser with most posts:", top_user)