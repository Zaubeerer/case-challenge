from typing import Any

from banking_api.models import Account, AccountCreate
from fastapi import APIRouter, HTTPException

from ..database import SessionDep

router = APIRouter()


class AccountNotFound(HTTPException):
    pass


@router.get("/", response_model=list[Account])
def list_accounts(session: SessionDep) -> Any:
    """
    Retrieve a list of all accounts from the session.
    """
    accounts = session.query(Account).all()
    return accounts


@router.post("/", response_model=Account)
def create_account(account_in: AccountCreate, session: SessionDep) -> Any:
    """
    Creates a new account.
    """
    account = Account.model_validate(account_in)

    session.add(account)
    session.commit()
    session.refresh(account)

    return account


@router.get("/{account_id}/balance", response_model=float)
def get_account_balance(account_id: int, session: SessionDep) -> Any:
    """
    Retrieve the balance of a specific account.
    """
    account = session.query(Account).get(account_id)
    if account:
        return account.balance
    else:
        raise AccountNotFound(
            status_code=404, detail=f"Account with {account_id=} not found"
        )
