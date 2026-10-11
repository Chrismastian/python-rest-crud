# python-rest-crud

[![CI](https://github.com/Chrismastian/python-rest-crud/actions/workflows/ci.yml/badge.svg)](https://github.com/Chrismastian/python-rest-crud/actions/workflows/ci.yml)

REST API CRUD sederhana pakai **stdlib `http.server`** (tanpa dependency) untuk belajar Python: HTTP mentah (method, status code, JSON body), file I/O, dan testing integrasi.

## Cara pakai

```bash
python -m rest.server          # jalan di http://localhost:8000
```

Lalu dari terminal lain:

```bash
curl http://localhost:8000/items
curl -X POST http://localhost:8000/items -d '{"name":"belajar REST"}'
curl http://localhost:8000/items/1
curl -X PUT http://localhost:8000/items/1 -d '{"name":"updated"}'
curl -X DELETE http://localhost:8000/items/1
```

Data disimpan di `data.json` (dibuat otomatis).

## Endpoint

| Method | URL | Fungsi | Status |
|--------|-----|--------|--------|
| GET | `/items` | semua item | 200 |
| GET | `/items/{id}` | satu item | 200 / 404 |
| POST | `/items` | bikin baru | 201 / 400 |
| PUT | `/items/{id}` | update | 200 / 400 / 404 |
| DELETE | `/items/{id}` | hapus | 200 / 404 |

## Development

```bash
pip install pytest
pytest
```

## Struktur

```
rest/
  store.py   # data layer: list of dict + simpan ke JSON
  server.py  # HTTP layer: baca method+URL, panggil store, balas JSON
tests/
  test_store.py    # unit test logic
  test_server.py   # integration test (start server, tembak pakai urllib)
```
