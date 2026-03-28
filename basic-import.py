import requests

# Public API (no key needed)
url = "https://jsonplaceholder.typicode.com/posts" # public api 

response = requests.get(url)

print("Status Code:", response.status_code)

# Print first 2 results
data = response.json()
print(data[:2])
# REQUEST API