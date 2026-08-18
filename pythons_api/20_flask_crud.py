"""Real implementation: a Flask REST API (CRUD).

Run:
    pip install flask
    python 20_flask_crud.py
Then open http://127.0.0.1:5000/items in a browser, or curl it:
    curl http://127.0.0.1:5000/items
    curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d '{"name":"laptop"}'
"""

import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory store (a real app would use a database - see files 29/30)
items: dict[str, dict] = {}


# ------------------------------------------------------------------- helpers
def error(message: str, code: str, status: int):
    return jsonify({"error": {"code": code, "message": message}}), status


def serialize(item: dict) -> dict:
    return {"id": item["id"], "name": item["name"], "created_at": item["created_at"]}


# ------------------------------------------------------------------ endpoints
@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/items")
def list_items():
    """GET /items?page=1&limit=10 - paginated list."""
    page = max(1, request.args.get("page", 1, type=int))
    limit = min(100, max(1, request.args.get("limit", 10, type=int)))

    all_items = list(items.values())
    start = (page - 1) * limit
    data = all_items[start:start + limit]

    return jsonify({
        "data": [serialize(i) for i in data],
        "meta": {"page": page, "limit": limit, "total": len(all_items)},
    })


@app.get("/items/<item_id>")
def get_item(item_id: str):
    item = items.get(item_id)
    if item is None:
        return error("Item not found", "ITEM_NOT_FOUND", 404)
    return jsonify(serialize(item))


@app.post("/items")
def create_item():
    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name or not isinstance(name, str):
        return error("A non-empty string 'name' is required", "VALIDATION_ERROR", 400)

    item = {"id": uuid.uuid4().hex, "name": name.strip(), "created_at": __import__("datetime").datetime.utcnow().isoformat() + "Z"}
    items[item["id"]] = item
    return jsonify(serialize(item)), 201


@app.put("/items/<item_id>")
def update_item(item_id: str):
    item = items.get(item_id)
    if item is None:
        return error("Item not found", "ITEM_NOT_FOUND", 404)

    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name or not isinstance(name, str):
        return error("A non-empty string 'name' is required", "VALIDATION_ERROR", 400)

    item["name"] = name.strip()
    return jsonify(serialize(item))


@app.patch("/items/<item_id>")
def patch_item(item_id: str):
    item = items.get(item_id)
    if item is None:
        return error("Item not found", "ITEM_NOT_FOUND", 404)

    body = request.get_json(silent=True) or {}
    if "name" in body:
        if not isinstance(body["name"], str) or not body["name"].strip():
            return error("'name' must be a non-empty string", "VALIDATION_ERROR", 400)
        item["name"] = body["name"].strip()
    return jsonify(serialize(item))


@app.delete("/items/<item_id>")
def delete_item(item_id: str):
    if item_id not in items:
        return error("Item not found", "ITEM_NOT_FOUND", 404)
    del items[item_id]
    return "", 204


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
