import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/comments"
data = requests.get(url).json()

df = pd.DataFrame(data)

# Save to CSV
df.to_csv("comments_data.csv", index=False)

print("Data saved to comments_data.csv")