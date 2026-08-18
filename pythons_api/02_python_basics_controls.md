# Python Basics & Control Flow

Everything in Python is about *flow of control*. Before calling APIs you need to
master these building blocks.

## 1. Variables & Data Types

```python
name = "Sanjog"      # str
age = 25             # int
height = 5.9         # float
is_active = True     # bool
tags = ["a", "b"]    # list
config = {"key": 1}  # dict
```

## 2. Conditional statements

```python
if status == 200:
    print("OK")
elif status == 404:
    print("Not Found")
else:
    print("Other")
```

The `match` statement (Python 3.10+):

```python
match status:
    case 200: print("OK")
    case 404: print("Not Found")
    case _:   print("Other")
```

## 3. Loops

```python
# for loop over a range
for i in range(3):
    print(i)

# for loop over a collection
for page in pages:
    fetch(page)

# while loop (great for retry logic)
attempts = 0
while attempts < 5:
    try_api_call()
    attempts += 1

# break / continue / else
for item in items:
    if item is None:
        continue
    if item == "stop":
        break
```

## 4. Comprehensions (idiomatic Python)

```python
squares = [x * x for x in range(10)]
even    = [x for x in range(10) if x % 2 == 0]
lookup  = {key: value for key, value in pairs}
```

## 5. Functions

```python
def get_user(user_id: int, include_email: bool = False) -> dict:
    ...
    return {}
```

- Positional args, keyword args, `*args`, `**kwargs`.
- `lambda` for short inline functions.
- Default values, docstrings, type hints.

## 6. Exception handling

```python
try:
    response = session.get(url, timeout=5)
    response.raise_for_status()
except requests.Timeout:
    log("timed out")
except requests.HTTPError as e:
    log(f"HTTP error: {e.response.status_code}")
else:
    return response.json()
finally:
    session.close()
```

## 7. Context managers

```python
with open("data.json", "w") as f:
    json.dump(payload, f)

with requests.Session() as s:
    r = s.get(url)
```

## 8. Classes

```python
class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str) -> dict:
        ...
```

Use classes to encapsulate API logic. Use dataclasses for models:

```python
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
```

Practice these in the accompanying `.py` files. Controls are the grammar; APIs
are the conversation.
