from model import User
from security import hash_password
from jose import jwt
from datetime import datetime, timedelta, timezone
from security import SECRET_KEY, ALGORITHM
def test_create_user(client):
    response = client.post(
        "/users/create",
        json={
            "username":"testuser",
            "email":"test@gmail.com",
            "password":"testpass123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_already_existed(client, db_session):
    user = User(username = "testuser", email = "test@gmail.com",hashed_password =hash_password("testpass123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.post(
        "users/create",
        json={
             "username":"testuser",
                "email":"test@gmail.com",
                    "password":"testpass123"
                }
    )
    assert response.status_code == 409

def test_create_user_with_existed_email(client, db_session):
    user = User(username = "testuser", email = "test@gmail.com",hashed_password =hash_password("testpass123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.post(
        "users/create",
       json={
                    "username":"testuser1",
                       "email":"test@gmail.com",
                           "password":"testpass123"
                       }
    )

    assert response.status_code == 409


def test_create_user_with_missing_field(client, db_session):
    response = client.post(
        "users/create",
        json={
            "username":"testuser",
            "email":"test@gmail.com"
        }
    )

    assert response.status_code ==422

def test_login_with_access_token(client,db_session):
    user = User(username = "testuser", email = "test@gmail.com",hashed_password =hash_password("testpass123"))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    response = client.post("/users/login", data={
            "username":"testuser",
            "password":"testpass123"
        })
    assert response.status_code == 200
    access_token= response.json()["access_token"]

    assert access_token is not None
def test_login_with_wrong_password(client, auth_token):
    response = client.post(
        "/users/login",
        data={
            "username": "testuser",
            "password": "1",
        }
    )
    assert response.status_code == 404

def test_login_with_unexisted_username(client,auth_token):
    response = client.post(
        "/users/login",
        data= {
            "username" : "testuser1",
            "password" : "1"
        }
    )
    print("STATUS:", response.status_code)
    print("BODY:", response.text)
    print("JSON:", response.json())
    print("HEADERS:", response.headers)
    assert response.status_code == 404


def test_get_all_user_admin(client, db_session,login_admin):
    response = client.get(
        "/users/all",
        headers={"Authorization" : f"Bearer {login_admin}"}
    )


    assert response.status_code == 200

def test_get_all_user_normal(client,auth_token):

    response = client.get(
        "/users/all",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 403

def test_get_my_profile(client, auth_token):
    response = client.get(
        "/users/me",
        headers={"Authorization" : f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
def test_get_my_profile_without_token(client):
    response = client.get(
        "/users/me"
    )
    assert response.status_code == 401

def test_get_my_profile_invalid_format_token(client,auth_token):
    response = client.get(
        "/users/me",
        headers={"Authorization" : f"Bearer{auth_token}"}
    )
    assert response.status_code == 401


def test_get_my_profile_with_forged_token(client):
    forged_token = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
        "WRONG_SECRET_KEY",          # ← secret khác
        algorithm="HS256",
    )


    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {forged_token}"},
    )

    assert response.status_code == 404
def test_get_my_profile_with_expired_token(client, db_session):
    # Tạo user trước để token trỏ tới user tồn tại
    user = User(
        username="testuser",
        email="test@gmail.com",
        hashed_password=hash_password("testpass123"),
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Token hết hạn 1 giờ trước
    expired_token = jwt.encode(
        {
            "sub": str(user.id),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"},
    )

    assert response.status_code == 404, response.text

def test_get_user_profile(login_admin,client,db_session):
    users = [
        User(
                username="testuser",
                email="test@gmail.com",
                hashed_password=hash_password("testpass123"),
            ),
        User(
                          username="testuser2",
                          email="test2@gmail.com",
                          hashed_password=hash_password("testpass123"),
                      )  
    ]
    db_session.add_all(users)
    db_session.commit()

    for u in users:
        db_session.refresh(u)
    
    response = client.get(
        "/users/2",
        headers={"Authorization":f"Bearer {login_admin}"}

    )

    assert response.status_code == 200

def test_get_user_not_existed(login_admin,client):
    response = client.get(
        "/users/2",
        headers={"Authorization": f"Bearer {login_admin}"}
    )

    assert response.status_code == 404