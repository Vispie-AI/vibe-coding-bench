"""Smoke tests — confirm generation RUNS. They say nothing about quality."""
from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)
KEY = {"x-api-key": "sk_live_demo"}  # demo api key


def test_generate_returns_200():
    r = client.post("/generate", json={"creator_id": "c_1", "brief": "new shoe drop"}, headers=KEY)
    assert r.status_code == 200
    assert r.json()["caption"]  # non-empty


def test_regenerate_runs():
    g = client.post("/generate", json={"creator_id": "c_1", "brief": "x"}, headers=KEY).json()
    r = client.post("/regenerate", json={"creator_id": "c_1", "item_id": g["item_id"]}, headers=KEY)
    assert r.status_code == 200
    # NOTE: we do not assert anything about the quality or
    # style-consistency of the regenerated creative.
