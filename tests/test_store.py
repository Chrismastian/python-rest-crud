from rest import store


def test_create_assigns_ids():
    items = []
    a = store.create(items, "kopi")
    b = store.create(items, "teh")
    assert a == {"id": 1, "name": "kopi"}
    assert b["id"] == 2
    assert len(items) == 2


def test_get_one():
    items = [{"id": 1, "name": "kopi"}]
    assert store.get_one(items, 1) == {"id": 1, "name": "kopi"}
    assert store.get_one(items, 99) is None


def test_update():
    items = [{"id": 1, "name": "kopi"}]
    result = store.update(items, 1, "teh")
    assert result == {"id": 1, "name": "teh"}
    assert items[0]["name"] == "teh"
    assert store.update(items, 99, "x") is None


def test_delete():
    items = [{"id": 1, "name": "kopi"}, {"id": 2, "name": "teh"}]
    removed = store.delete(items, 1)
    assert removed == {"id": 1, "name": "kopi"}
    assert len(items) == 1
    assert store.delete(items, 99) is None


def test_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "data.json"
    store.save([{"id": 1, "name": "kopi"}], path)
    assert store.load(path) == [{"id": 1, "name": "kopi"}]
