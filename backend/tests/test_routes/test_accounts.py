import pytest
from banking_api.routes.accounts import AccountNotFound
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


@pytest.mark.parametrize(
    "account_id, expected_value, status_code, expected_exception",
    [
        pytest.param(1, 1000.0, 200, None, id="account_exists"),
        pytest.param(
            3,
            {"detail": "Account with account_id=3 not found"},
            404,
            AccountNotFound,
            id="account_not_found",
        ),
    ],
)
def test_get_account_balance(
    client_with_accounts: TestClient,
    account_id: int,
    expected_value: float | str,
    status_code: int,
    expected_exception: Exception | None,
):
    response = client_with_accounts.get(f"/accounts/{account_id}/balance")
    assert response.status_code == status_code
    assert response.json() == expected_value


def test_list_accounts(client: TestClient):
    response = client.get("/accounts/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
