from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from .models import Customer

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables(engine=engine):
    SQLModel.metadata.create_all(engine)


def clear_data(session: Session):
    session.execute(text("DELETE FROM customer"))
    session.commit()


def populate_db(engine=engine):
    initial_customers = [
        {"id": 1, "name": "Arisha Barron"},
        {"id": 2, "name": "Branden Gibson"},
        {"id": 3, "name": "Rhonda Church"},
        {"id": 4, "name": "Georgina Hazel"},
    ]

    with Session(engine) as session:
        customers = [
            Customer(name=customer["name"], id=customer["id"])
            for customer in initial_customers
        ]
        session.add_all(customers)
        accounts = []
        session.add_all(accounts)
        session.commit()


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
