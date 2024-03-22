import pytest
from banking_api.models import TransferCreate
from banking_api.routes.transfers import InsufficientFunds
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "amount, expected_response, expected_exception",
    [
        pytest.param(
            100.0,
            {"id_sender": 1, "id_receiver": 2, "amount": 100.0, "id": None},
            None,
            id="transfer successful",
        ),
        pytest.param(2000.0, None, InsufficientFunds, id="transfer failed"),
    ],
)
def test_transfer_amount(
    client_with_accounts: TestClient,
    amount: float,
    expected_response: dict | None,
    expected_exception: Exception | None,
):
    transfer_data = {
        "id": 1,
        "amount": amount,
        "id_sender": 1,
        "id_receiver": 2,
    }

    transfer_create = TransferCreate(**transfer_data)

    if expected_exception is not None:
        with pytest.raises(expected_exception):
            response = client_with_accounts.post(
                "/transfers", json=transfer_create.dict()
            )
    else:
        response = client_with_accounts.post("/transfers", json=transfer_create.dict())

        assert response.status_code == 200
        assert response.json() == expected_response
