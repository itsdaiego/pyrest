import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime

from app.main import app
from app.db.database import Base, get_db
from app.models.user import User, Profile
from app.models.contract import Contract, ContractStatus
from app.models.job import Job

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



def test_process_job_payment(client):
    db = TestingSessionLocal()
    
    print("oi")
    client_user = User(
        username="myusernameyeah",
        email="client@example.com",
        profile=Profile.CLIENT,
        hashed_password="123"

    )
    contractor_user = User(
        username="myusernameyeah2",
        email="contractor@example.com",
        profile=Profile.CONTRACTOR,
        hashed_password="123"
    )
    db.add_all([client_user, contractor_user])
    db.commit()

    contract = Contract(
        title="Test Contract",
        description="Test Description",
        price=1000,
        client_id=client_user.id,
        contractor_id=contractor_user.id,
        status=ContractStatus.ACTIVE
    )
    db.add(contract)
    db.commit()

    job = Job(
        description="Test Job",
        price=500,
        paid=False,
        payment_date=datetime.utcnow(),
        contract=contract.id
    )
    db.add(job)
    db.commit()

    payment_date = datetime.utcnow()
    response = client.post(
        "/jobs/process_payment",
        json={"job_id": job.id, "payment_date": payment_date.isoformat()}
    )

    assert response.status_code == 200
    assert response.json()["paid"] == True
    assert response.json()["payment_date"] is not None

    db.close()
