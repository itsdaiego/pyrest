import pytest

from app.models.user import Profile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base, get_db
from tests.test_user import SQLALCHEMY_DATABASE_URL
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def create_user(client):
    response_client = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "testpassword",
            "profile": Profile.CLIENT.value,
        }
    )

    response_contractor = client.post(
        "/auth/register",
        json={
            "username": "testuser2",
            "email": "test2@email.com",
            "password": "testpassword",
            "profile": Profile.CONTRACTOR.value,
        }
    )

    return (response_client.json()['id'], response_contractor.json()['id'])


def test_create_contract(client):
    (client_profile, contractor_profile) = create_user(client)

    response = client.post(
        "/contracts/",
        json={
            "title": "Test Contract",
            "description": "Test description",
            "price": 1000.00,
            "client_id": client_profile,
            "contractor_id": contractor_profile
        }
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "Test Contract"
    assert response.json()["description"] == "Test description"
    assert response.json()["price"] == 1000.00
    assert response.json()["client_id"] == client_profile
    assert response.json()["contractor_id"] == contractor_profile
    assert "created_at" in response.json()
    assert "updated_at" in response.json()
    assert "status" in response.json()
