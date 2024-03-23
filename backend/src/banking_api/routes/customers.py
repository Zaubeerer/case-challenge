from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..database import SessionDep
from ..models import Account, Customer, CustomerCreate

router = APIRouter()


@router.get("/", response_model=list[Customer])
def read_customers(session: SessionDep) -> Any:
    """
    Retrieve all customers.
    """
    customers = session.exec(select(Customer)).all()
    return customers


@router.post("/", response_model=Customer)
def create_customer(customer_in: CustomerCreate, session: SessionDep) -> Any:
    """
    Create new customer.
    """
    customer = Customer.model_validate(customer_in)

    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.get("/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, session: SessionDep) -> Any:
    """
    Retrieve a single customer based on its customer ID.
    """
    customer = session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, session: SessionDep) -> Any:
    """
    Delete a customer.
    """
    customer = session.exec(select(Customer).where(Customer.id == customer_id)).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return customer


@router.get("/{customer_id}/accounts", response_model=list[Account])
def list_accounts_by_customer(customer_id: int, session: SessionDep) -> Any:
    """
    Retrieve all accounts for a given customer ID.
    """
    accounts = session.query(Account).filter(Account.customer_id == customer_id).all()
    return accounts
