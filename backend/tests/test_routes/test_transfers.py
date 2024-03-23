import pytest
from banking_api.models import Transfer, TransferCreate
from banking_api.routes.transfers import AccountIDError, InsufficientFunds
from conftest import TRANSFER
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "transfer_data, expected_response, expected_exception",
    [
        pytest.param(
            {
                "id": 1,
                "amount": 100.0,
                "id_sender": 1,
                "id_receiver": 2,
            },
            TransferCreate(
                **{"id_sender": 1, "id_receiver": 2, "amount": 100.0, "id": 1}
            ),
            None,
            id="transfer successful",
        ),
        pytest.param(
            {
                "id": 1,
                "amount": 2000.0,
                "id_sender": 1,
                "id_receiver": 2,
            },
            None,
            InsufficientFunds,
            id="transfer failed",
        ),
        pytest.param(
            {
                "id": 1,
                "amount": 2000.0,
                "id_sender": 10,
                "id_receiver": 2,
            },
            None,
            AccountIDError,
            id="transfer failed",
        ),
        pytest.param(
            {
                "id": 1,
                "amount": 2000.0,
                "id_sender": 1,
                "id_receiver": 10,
            },
            None,
            AccountIDError,
            id="transfer failed",
        ),
    ],
)
def test_transfer_amount(
    client_with_accounts: TestClient,
    transfer_data: dict,
    expected_response: dict | None,
    expected_exception: Exception | None,
):
    transfer_create = TransferCreate(**transfer_data)

    if expected_exception is not None:
        with pytest.raises(expected_exception):
            response = client_with_accounts.post(
                "/transfers", json=transfer_create.dict()
            )
    else:
        response = client_with_accounts.post("/transfers", json=transfer_create.dict())

        assert response.status_code == 200
        assert TransferCreate(**response.json()) == expected_response


def test_get_transfer_history(client_with_transfers: TestClient):
    response = client_with_transfers.get("/transfers/history")

    assert response.status_code == 200

    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    for transfer in response.json():
        assert TransferCreate(**transfer) == TRANSFER


@pytest.mark.parametrize("account_id, expected_transfers", [(1, [TRANSFER]), (3, [])])
def test_get_transfer_history_by_account_id(
    client_with_transfers: TestClient,
    account_id: int,
    expected_transfers: list[Transfer],
):
    response = client_with_transfers.get(f"/transfers/history/{account_id}")

    assert response.status_code == 200

    assert isinstance(response.json(), list)
    assert len(response.json()) == len(expected_transfers)
    for transfer_dict in response.json():
        transfer = TransferCreate(**transfer_dict)
        assert transfer.id_sender == account_id or transfer.id_receiver == account_id
