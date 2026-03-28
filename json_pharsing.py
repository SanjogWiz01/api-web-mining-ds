import requests

url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

users = response.json()

# Extract specific fields
for user in users:
    name = user['name']
    email = user['email']
    city = user['address']['city']

    print(f"Name: {name}, Email: {email}, City: {city}")