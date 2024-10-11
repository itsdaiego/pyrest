import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base
from app.db import get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_success():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_register_existing_user():
    client.post(
        "/register",
        json={
            "username": "existinguser",
            "email": "existinguser@example.com",
            "password": "testpassword"
        }
    )
    
    response = client.post(
        "/register",
        json={
            "username": "existinguser",
            "email": "existinguser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "User already exists"

def test_register_invalid_email():
    response = client.post(
        "/register",
        json={
            "username": "invaliduser",
            "email": "notanemail",
            "password": "testpassword"
        }
    )
    assert response.status_code == 422 

def test_register_missing_fields():
    response = client.post(
        "/register",
        json={
            "username": "missinguser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 422 
