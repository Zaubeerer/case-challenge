from fastapi.testclient import TestClient


def test_read_customers(client: TestClient):
    response = client.get("customers/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Arisha Barron"},
        {"id": 2, "name": "Branden Gibson"},
        {"id": 3, "name": "Rhonda Church"},
        {"id": 4, "name": "Georgina Hazel"},
    ]


def test_create_customer(client: TestClient):
    response = client.post("customers/", json={"name": "John Doe"})
    assert response.status_code == 200
    assert response.json() == {"id": 5, "name": "John Doe"}


def test_read_customer(client: TestClient):
    response = client.get("customers/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Arisha Barron"}


def test_delete_customer(client: TestClient):
    response = client.delete("customers/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Arisha Barron"}
