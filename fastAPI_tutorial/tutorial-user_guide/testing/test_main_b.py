"""Extended testing file"""
# It has a GET operation that could return an error.
# It has a POST operation that could return several errors.
# Both path operations require an X-Token header.

from fastapi.testclient import TestClient

from .main_b import app

client = TestClient(app)


def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {
            "id": "foo",
            "title": "Foo",
            "description": "There goes my hero",
            }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
            "/items/",
            headers={"X-Token": "coneofsilence"},
            json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
            )
    assert response.status_code == 200
    assert response.json() == {
            "id": "foobar",
            "title": "Foo Bar",
            "description": "The Foo Barters",
            }

# Info
# Note that the `TestClient` receives data that can be converted to JSON, 
    # NOT Pydantic models.
# If you have a Pydantic model in your test 
# and you want to send its data to the application during testing, 
# you can use the jsonable_encoder desceibed in JSON Compatible Encoder.
def test_create_item_bad_token():
    response = client.post(
            "/items/",
            headers={"X-Token": "hailhydra"},
            json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
            )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
            "/items/",
            headers={"X-Token": "coneofsilence"},
            json={
                    "id": "foo",
                    "title": "The Foo ID Stealers",
                    "description": "There goes my stealer",
                    },
            )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}
