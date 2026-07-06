from fastapi import APIRouter

router = APIRouter()


@router.get("/items")
def get_items():
    return [{"id": 1, "name": "Item 1"}]


@router.get("/items/{item_id}")
def get_item(item_id: int):
    return {"id": item_id, "name": f"Item {item_id}"}
