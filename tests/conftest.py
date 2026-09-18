import os 
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


load_dotenv()


from database import Base, get_db
from main import app
import model


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
test_engine = create_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = sessionmaker(bind=test_engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture 
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def auth_token(client):
    client.post("users/create", json={
        "username":"testuser",
        "email":"test@gmail.com",
        "password":"testpass123"
    })
    response = client.post("/users/login", data={
        "username":"testuser",
        "password":"testpass123"
    })

    return response.json()["access_token"]