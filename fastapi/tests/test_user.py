import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.db.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


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

def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

def test_register_existing_user(client):
    client.post(
        "/auth/register",
        json={
            "username": "existinguser",
            "email": "existinguser@example.com",
            "password": "testpassword"
        }
    )
    
    response = client.post(
        "/auth/register",
        json={
            "username": "existinguser",
            "email": "existinguser@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "User already exists"

def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "invaliduser",
            "email": "notanemail",
            "password": "testpassword"
        }
    )

    assert response.status_code == 422 

def test_register_missing_fields(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "missinguser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 422 


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "testpassword",
        }
    )

    response = client.post(
        '/auth/login',
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200

    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_invalid_credentials(client):
    client.post(
        "/auth/register",
        json={
            "username": "testuser",
            "email": "test@email.com",
            "password": "testpassword",
        }
    )

    response = client.post(
        '/auth/login',
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


