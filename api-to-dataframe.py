import requests
import pandas as pd

url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)

data = response.json()

df = pd.DataFrame(data)

print(df.head())

# Show structure
print(df.info()) # pandas