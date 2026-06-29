# FastAPI Quick Start (5 minutes)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install fastapi uvicorn pydantic python-multipart
```

## Step 2: Run the Server

```bash
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process
```

## Step 3: Test the API

### Option A: Interactive Docs (Easiest!)
Open your browser and go to:
- **Interactive UI (Swagger)**: http://127.0.0.1:8000/docs
- **Alternative UI (ReDoc)**: http://127.0.0.1:8000/redoc

### Option B: curl Commands

```bash
# 1. Get all items
curl http://127.0.0.1:8000/items

# 2. Get a single item
curl http://127.0.0.1:8000/items/1

# 3. Create a new item
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Keyboard",
    "price": 149.99,
    "description": "Mechanical Keyboard",
    "is_available": true
  }'

# 4. Update an item
curl -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "price": 1599.99,
    "description": "High-end gaming laptop",
    "tax": 160.00
  }'

# 5. Delete an item
curl -X DELETE http://127.0.0.1:8000/items/2

# 6. Search items
curl "http://127.0.0.1:8000/items/search/by-name?q=laptop"

# 7. Health check
curl http://127.0.0.1:8000/health
```

### Option C: Python Requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Get all items
response = requests.get(f"{BASE_URL}/items")
print(response.json())

# Create an item
new_item = {
    "name": "Mouse Pad",
    "price": 19.99,
    "description": "Ergonomic Mouse Pad"
}
response = requests.post(f"{BASE_URL}/items", json=new_item)
print(response.json())
```

## Understanding the Code

### Pydantic Models (Data Validation)
```python
class Item(BaseModel):
    name: str           # Required field
    price: float        # Required field
    description: str = None  # Optional field with default
```

### Endpoints
```python
@app.get("/items")           # GET request
@app.post("/items")          # POST request (create)
@app.put("/items/{id}")      # PUT request (update)
@app.delete("/items/{id}")   # DELETE request
```

### Path Parameters
```python
@app.get("/items/{item_id}")  # item_id comes from URL
def get_item(item_id: int):
    return item
```

### Query Parameters
```python
@app.get("/items")
def get_items(skip: int = 0, limit: int = 10):  # From URL query string
    # Example: /items?skip=5&limit=20
    return items[skip:skip + limit]
```

## Common Patterns

### Check if item exists
```python
if item_id not in fake_items_db:
    raise HTTPException(status_code=404, detail="Not found")
```

### Return custom status code
```python
@app.post("/items", status_code=201)  # 201 = Created
def create_item(item: Item):
    return item
```

### Optional parameters
```python
@app.get("/search")
def search(q: str = None):  # Optional, defaults to None
    pass
```

## Next Steps

1. ✅ Run the app and test endpoints
2. 📖 Read the full README.md for concepts
3. 🔧 Modify main.py - change item fields, add new routes
4. 🗄️ Replace fake_items_db with a real database (SQLAlchemy)
5. 🔐 Add authentication/security
6. 📝 Add input validation
7. 🚀 Deploy to a server

## Troubleshooting

**Port 8000 already in use?**
```bash
uvicorn main:app --port 8001
```

**ModuleNotFoundError?**
```bash
pip install fastapi uvicorn pydantic
```

**Change not reflecting?**
- Make sure you're using `--reload` flag
- Restart the server with CTRL+C then re-run

## API Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | / | Welcome message |
| GET | /items | Get all items |
| GET | /items/{id} | Get single item |
| POST | /items | Create new item |
| PUT | /items/{id} | Update item |
| DELETE | /items/{id} | Delete item |
| GET | /items/search/by-name | Search items |
| GET | /items/{id}/details | Get detailed info |
| POST | /items/bulk-create | Create multiple |
| GET | /users | Get all users |
| GET | /users/{id} | Get single user |
| POST | /users | Create new user |
| GET | /health | Health check |

---

That's it! You're ready to start learning FastAPI! 🚀
