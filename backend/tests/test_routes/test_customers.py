import pytest
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


@pytest.mark.parametrize(
    "customer_id, status_code, expected_response",
    [
        (1, 200, {"id": 1, "name": "Arisha Barron"}),
        (10, 404, {"detail": "Customer not found"}),
    ],
)
def test_read_customer(
    client: TestClient,
    customer_id: int,
    status_code: int,
    expected_response: dict,
):
    response = client.get(f"customers/{customer_id}")
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "customer_id, status_code, expected_response",
    [
        (1, 200, {"id": 1, "name": "Arisha Barron"}),
        (10, 404, {"detail": "Customer not found"}),
    ],
)
def test_delete_customer(
    client: TestClient,
    customer_id: int,
    status_code: int,
    expected_response: dict,
):
    response = client.delete(f"customers/{customer_id}")
    assert response.status_code == status_code
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "customer_id, status_code, expected_response",
    [
        (4, 200, [{"id": 1, "customer_id": 4, "balance": 900.0}]),
        (10, 200, []),
    ],
)
def test_list_accounts_by_customer(
    client_with_transfers: TestClient,
    customer_id: int,
    status_code: int,
    expected_response: dict,
):
    response = client_with_transfers.get(f"/customers/{customer_id}/accounts")

    assert response.status_code == status_code
    assert response.json() == expected_response
