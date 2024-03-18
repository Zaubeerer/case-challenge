from typing import Any

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..database import create_db_and_tables, get_session, populate_db
from ..models import Customer

router = APIRouter()


@router.on_event("startup")
def on_startup():
    create_db_and_tables()
    populate_db()


@router.get("/", response_model=list[Customer])
def read_items(session: Session = Depends(get_session)) -> Any:
    """
    Retrieve items.
    """
    customers = session.exec(select(Customer)).all()
    return customers
