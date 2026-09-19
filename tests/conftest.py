import os 
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from model import User
from security import hash_password
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
    client.post("/users/create", json={
        "username":"testuser",
        "email":"test@gmail.com",
        "password":"testpass123"
    })
    response = client.post("/users/login", data={
        "username":"testuser",
        "password":"testpass123"
    })

    return response.json()["access_token"]
@pytest.fixture
def admin(client,db_session):
    admin = User(
        username = "admin",
        email = "admin@example.com",
        hashed_password= hash_password("admin123"),
        role ="admin"
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture 
def login_admin(admin,client):
    response = client.post(
        "/users/login",
        data={
            "username":"admin",
            "password":"admin123"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def example_author(db_session):
    author = model.Author(name="Nguyen Nhat Anh", country="Vietnam")
    db_session.add(author)
    db_session.commit()
    db_session.refresh(author)

    return author

@pytest.fixture
def sample_data(db_session):
    """Tạo 3 authors + 6 books, trả về dict {authors, books}."""
    authors = [
        model.Author(name="Nguyen Nhat Anh", country="Vietnam"),
        model.Author(name="Nguyen Du", country="Vietnam"),
        model.Author(name="Haruki Murakami", country="Japan"),
    ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    books = [
        # Nguyen Nhat Anh — 3 books
        model.Book(title="Nha Gia Kim", author_id=authors[0].id, published_year=2024),
        model.Book(title="Nhung Ke Xuat Chung", author_id=authors[0].id, published_year=2025),
        model.Book(title="Mat Biec", author_id=authors[0].id, published_year=2019),
        # Nguyen Du — 1 book
        model.Book(title="Truyen Kieu", author_id=authors[1].id, published_year=1820),
        # Haruki Murakami — 2 books
        model.Book(title="Norwegian Wood", author_id=authors[2].id, published_year=1987),
        model.Book(title="Kafka On The Shore", author_id=authors[2].id, published_year=2002),
    ]
    db_session.add_all(books)
    db_session.commit()
    for b in books:
        db_session.refresh(b)

    return {"authors": authors, "books": books}