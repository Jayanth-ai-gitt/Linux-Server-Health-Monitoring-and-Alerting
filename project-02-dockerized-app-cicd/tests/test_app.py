import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app  # noqa: E402


def client():
    return app.test_client()


def test_home():
    res = client().get("/")
    assert res.status_code == 200
    assert "message" in res.get_json()


def test_health():
    res = client().get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_time():
    res = client().get("/time")
    assert res.status_code == 200
    assert "utc" in res.get_json()


def test_unknown_route_returns_404():
    assert client().get("/nope").status_code == 404
