"""Data layer: list of dict + simpan ke file JSON."""
import json
from pathlib import Path

DATA_FILE = Path("data.json")


def load(path=DATA_FILE):
    if not path.exists():
        return []
    return json.loads(path.read_text("utf-8"))


def save(items, path=DATA_FILE):
    path.write_text(json.dumps(items, indent=2), "utf-8")


def get_all(items):
    return items


def get_one(items, item_id):
    for it in items:
        if it["id"] == item_id:
            return it
    return None


def create(items, name):
    next_id = max((it["id"] for it in items), default=0) + 1
    item = {"id": next_id, "name": name}
    items.append(item)
    return item


def update(items, item_id, name):
    item = get_one(items, item_id)
    if item is None:
        return None
    item["name"] = name
    return item


def delete(items, item_id):
    for i, it in enumerate(items):
        if it["id"] == item_id:
            return items.pop(i)
    return None
