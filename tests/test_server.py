import json
import threading
import urllib.error
import urllib.request
from http.server import HTTPServer

import pytest

from rest import server


@pytest.fixture
def base_url(tmp_path, monkeypatch):
    """Start the server on a random port in a thread; chdir to tmp so data is isolated."""
    monkeypatch.chdir(tmp_path)
    httpd = HTTPServer(("localhost", 0), server.Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://localhost:{httpd.server_port}"
    httpd.shutdown()
    thread.join()


def request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


def test_crud_flow(base_url):
    # empty first
    assert request("GET", f"{base_url}/items") == (200, [])

    # create
    status, item = request("POST", f"{base_url}/items", {"name": "coffee"})
    assert status == 201
    assert item == {"id": 1, "name": "coffee"}

    # read one
    assert request("GET", f"{base_url}/items/1") == (200, {"id": 1, "name": "coffee"})

    # update
    status, item = request("PUT", f"{base_url}/items/1", {"name": "tea"})
    assert status == 200
    assert item["name"] == "tea"

    # delete
    assert request("DELETE", f"{base_url}/items/1") == (200, {"id": 1, "name": "tea"})
    assert request("GET", f"{base_url}/items") == (200, [])


def test_not_found(base_url):
    assert request("GET", f"{base_url}/items/99")[0] == 404
    assert request("PUT", f"{base_url}/items/99", {"name": "x"})[0] == 404
    assert request("DELETE", f"{base_url}/items/99")[0] == 404


def test_bad_input(base_url):
    assert request("POST", f"{base_url}/items", {})[0] == 400
    assert request("POST", f"{base_url}/items", None)[0] == 400
