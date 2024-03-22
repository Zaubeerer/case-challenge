from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class CustomerCreate(SQLModel):
    name: str


class Customer(CustomerCreate, table=True):
    id: int = Field(default=None, primary_key=True)
    accounts: list["Account"] = Relationship(back_populates="customer")


class AccountCreate(SQLModel):
    customer_id: int = Field(foreign_key="customer.id", nullable=False)
    balance: float


class Account(AccountCreate, table=True):
    id: int = Field(default=None, primary_key=True)
    customer: Customer = Relationship(back_populates="accounts")


class TransferCreate(SQLModel):
    id_sender: int
    id_receiver: int
    amount: float


class Transfer(TransferCreate, table=True):
    id: int = Field(default=None, primary_key=True)
    executed_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow)
    )
