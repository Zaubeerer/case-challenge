from typing import Any

from fastapi import APIRouter
from sqlalchemy import or_
from sqlmodel import select

from ..database import SessionDep
from ..models import Account, Transfer, TransferCreate

router = APIRouter()


class AccountIDError(ValueError):
    pass


class InsufficientFunds(Exception):
    pass


@router.post("/", response_model=Transfer)
def transfer_amount(
    transfer_in: TransferCreate,
    session: SessionDep,
) -> Any:
    """
    Transfer the specified amount from one account to another.
    """
    with session:
        account_sender = session.exec(
            select(Account).where(Account.id == transfer_in.id_sender)
        ).first()
        account_receiver = session.exec(
            select(Account).where(Account.id == transfer_in.id_receiver)
        ).first()

        if not account_sender:
            raise AccountIDError(f"Account with {account_sender} does not exist.")

        elif not account_receiver:
            raise AccountIDError(f"Account with {account_receiver} does not exist.")

        if account_sender.balance < transfer_in.amount:
            raise InsufficientFunds(
                f"Sender's balance {account_sender.balance} is insufficient for a transfer of {transfer_in.amount}."
            )

        account_sender.balance -= transfer_in.amount
        account_receiver.balance += transfer_in.amount

        transfer = Transfer(**transfer_in.model_dump())
        session.add(transfer)
        session.commit()
        session.refresh(transfer)

    return transfer


@router.get("/history", response_model=list[Transfer])
def get_transfer_history(session: SessionDep) -> Any:
    """
    Retrieve the history of all transfers.
    """
    transfers = session.query(Transfer).all()
    return transfers


@router.get("/history/{account_id}", response_model=list[Transfer])
def get_transfer_history_by_account_id(account_id: int, session: SessionDep) -> Any:
    """
    Retrieves the transfer history for a given account ID.
    """
    transfers = (
        session.query(Transfer)
        .filter(
            or_(Transfer.id_sender == account_id, Transfer.id_receiver == account_id)
        )
        .all()
    )
    return transfers
