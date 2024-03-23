import pytest
from banking_api.database import create_db_and_tables, get_db, populate_db
from banking_api.main import app
from banking_api.models import TransferCreate
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

client = TestClient(app)


TRANSFER = TransferCreate(
    id=1,
    amount=100.0,
    id_sender=1,
    id_receiver=2,
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    populate_db(engine)
    create_db_and_tables(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)

    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_with_accounts(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    client.post(
        "accounts/",
        json={
            "balance": 1000.0,
            "customer_id": 4,
        },
    )
    client.post(
        "accounts/",
        json={
            "balance": 1000.0,
            "customer_id": 3,
        },
    )
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def client_with_transfers(client_with_accounts: TestClient):
    client_with_accounts.post("/transfers", json=TRANSFER.dict())

    yield client_with_accounts
    app.dependency_overrides.clear()
