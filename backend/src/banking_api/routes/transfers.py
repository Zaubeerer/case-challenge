from fastapi import APIRouter
from sqlalchemy import or_
from sqlmodel import select

from ..database import SessionDep, create_db_and_tables
from ..models import Account, Transfer, TransferCreate

router = APIRouter()


class AccountIDError(ValueError):
    pass


class InsufficientFunds(Exception):
    pass


@router.on_event("startup")
def on_startup():
    create_db_and_tables()


@router.post("/", response_model=Transfer)
def transfer_amount(
    transfer_in: TransferCreate,
    session: SessionDep,
):
    with session:
        account_sender = session.exec(
            select(Account).where(Account.id == transfer_in.id_sender)
        ).one()
        account_receiver = session.exec(
            select(Account).where(Account.id == transfer_in.id_receiver)
        ).one()

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

        transfer = Transfer(**transfer_in.dict())
        session.add(transfer)
        session.commit()
        session.refresh(transfer)

    return transfer


@router.get("/history", response_model=list[Transfer])
def get_transfer_history(session: SessionDep):
    transfers = session.query(Transfer).all()
    return transfers


@router.get("/history/{account_id}", response_model=list[Transfer])
def get_transfer_history_by_account_id(account_id: int, session: SessionDep):
    transfers = (
        session.query(Transfer)
        .filter(
            or_(Transfer.id_sender == account_id, Transfer.id_receiver == account_id)
        )
        .all()
    )
    return transfers
