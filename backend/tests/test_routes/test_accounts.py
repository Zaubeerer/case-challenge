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
    "account_id, expected_value, expected_exception",
    [
        pytest.param(1, 1000.0, None, id="account_exists"),
        pytest.param(3, None, AccountNotFound, id="account_not_found"),
    ],
)
def test_get_account_balance(
    client_with_accounts: TestClient, account_id, expected_value, expected_exception
):
    if expected_exception is not None:
        with pytest.raises(AccountNotFound):
            response = client_with_accounts.get(f"/accounts/{account_id}/balance")
    else:
        response = client_with_accounts.get(f"/accounts/{account_id}/balance")
        assert response.status_code == 200
        assert response.json() == expected_value
