"""HTTP layer: baca method+URL, panggil store, balas JSON."""
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

from rest import store


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _item_id(self):
        match = re.match(r"^/items/(\d+)$", self.path)
        return int(match.group(1)) if match else None

    def do_GET(self):
        items = store.load()
        item_id = self._item_id()
        if item_id is None:
            if self.path == "/items":
                self._send(200, items)
            else:
                self._send(404, {"error": "not found"})
            return
        item = store.get_one(items, item_id)
        if item is None:
            self._send(404, {"error": "not found"})
        else:
            self._send(200, item)

    def do_POST(self):
        if self.path != "/items":
            self._send(404, {"error": "not found"})
            return
        body = self._read_body()
        if not body or "name" not in body:
            self._send(400, {"error": "butuh field 'name'"})
            return
        items = store.load()
        item = store.create(items, body["name"])
        store.save(items)
        self._send(201, item)

    def do_PUT(self):
        item_id = self._item_id()
        body = self._read_body()
        if item_id is None or not body or "name" not in body:
            self._send(400, {"error": "butuh id dan field 'name'"})
            return
        items = store.load()
        item = store.update(items, item_id, body["name"])
        if item is None:
            self._send(404, {"error": "not found"})
            return
        store.save(items)
        self._send(200, item)

    def do_DELETE(self):
        item_id = self._item_id()
        if item_id is None:
            self._send(404, {"error": "not found"})
            return
        items = store.load()
        item = store.delete(items, item_id)
        if item is None:
            self._send(404, {"error": "not found"})
            return
        store.save(items)
        self._send(200, item)


def run(port=8000):
    server = HTTPServer(("localhost", port), Handler)
    print(f"Jalan di http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
