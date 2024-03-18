import pytest
from banking_api.database import create_db_and_tables, get_session, populate_db
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

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)

    yield client
    app.dependency_overrides.clear()


def test_read_main(client: TestClient):
    response = client.get("customers/")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "Arisha Barron"},
        {"id": 2, "name": "Branden Gibson"},
        {"id": 3, "name": "Rhonda Church"},
        {"id": 4, "name": "Georgina Hazel"},
    ]
