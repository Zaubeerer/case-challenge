from fastapi.testclient import TestClient


def test_create_bank_account(client: TestClient):
    response = client.post(
        "accounts/",
        json={
            "balance": 1000.0,
            "customer_id": 4,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "customer_id": 4, "balance": 1000.0}
