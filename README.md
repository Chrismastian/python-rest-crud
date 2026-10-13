# python-rest-crud

[![CI](https://github.com/Chrismastian/python-rest-crud/actions/workflows/ci.yml/badge.svg)](https://github.com/Chrismastian/python-rest-crud/actions/workflows/ci.yml)

A simple CRUD REST API built with the **stdlib `http.server`** (no dependencies) while learning Python: raw HTTP (methods, status codes, JSON bodies), file I/O, and integration testing.

## Usage

```bash
python -m rest.server          # runs at http://localhost:8000
```

Then from another terminal:

```bash
curl http://localhost:8000/items
curl -X POST http://localhost:8000/items -d '{"name":"learn REST"}'
curl http://localhost:8000/items/1
curl -X PUT http://localhost:8000/items/1 -d '{"name":"updated"}'
curl -X DELETE http://localhost:8000/items/1
```

Data is stored in `data.json` (created automatically).

## Endpoints

| Method | URL | Description | Status |
|--------|-----|-------------|--------|
| GET | `/items` | all items | 200 |
| GET | `/items/{id}` | one item | 200 / 404 |
| POST | `/items` | create | 201 / 400 |
| PUT | `/items/{id}` | update | 200 / 400 / 404 |
| DELETE | `/items/{id}` | delete | 200 / 404 |

## Development

```bash
pip install pytest
pytest
```

## Structure

```
rest/
  store.py   # data layer: list of dict + persist to JSON
  server.py  # HTTP layer: parse method+URL, call store, reply JSON
tests/
  test_store.py    # unit tests for logic
  test_server.py   # integration test (start server, hit it with urllib)
```
