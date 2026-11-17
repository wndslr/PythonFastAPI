from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="CRUD Service")

items_db: dict[int, dict] = {}
next_id = 1


class ItemIn(BaseModel):
    name: str
    description: Optional[str] = None


class Item(ItemIn):
    id: int


@app.get("/items", response_model=list[Item])
def list_items():
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemIn):
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    items_db[next_id] = new_item
    next_id += 1
    return new_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemIn):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = {"id": item_id, **item.model_dump()}
    items_db[item_id] = updated
    return updated


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None


@app.get("/")
def health():
    return {"status": "ok"}
