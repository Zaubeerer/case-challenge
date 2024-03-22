import pytest
from banking_api.database import create_db_and_tables, get_db, populate_db
from banking_api.main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

client = TestClient(app)


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


@pytest.fixture(name="client_with_account")
def client_fixture_with_account(session: Session):
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
    yield client
    app.dependency_overrides.clear()
