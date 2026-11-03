import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import create_app

def test_index():
    app = create_app()
    c = app.test_client()
    r = c.get("/")
    assert r.status_code == 200
    assert "БПЛА".encode() in r.data

def test_drone_detail_404():
    app = create_app()
    c = app.test_client()
    r = c.get("/drones/nope")
    assert r.status_code == 404

def test_generic_404_uses_error_template():
    app = create_app()
    c = app.test_client()
    r = c.get("/no-such-page")
    assert r.status_code == 404
    assert "404".encode() in r.data
