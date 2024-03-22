from banking_api.models import Account, AccountCreate
from fastapi import APIRouter

from ..database import SessionDep, create_db_and_tables

router = APIRouter()


@router.on_event("startup")
def on_startup():
    create_db_and_tables()


@router.get("/", response_model=list[Account])
def list_accounts(session: SessionDep):
    accounts = session.query(Account).all()
    return accounts


@router.post("/", response_model=Account)
def create_account(account_in: AccountCreate, session: SessionDep):
    account = Account.model_validate(account_in)

    session.add(account)
    session.commit()
    session.refresh(account)

    return account
