



def test_vote_book(client,auth_token,sample_data):
    response = client.post(
        "/votes/1/vote",
        headers={"Authorization":f"Bearer {auth_token}"}
    )

    assert response.status_code == 201

def test_unvote(client,auth_token, sample_data):
    client.post(
        "/votes/1/vote",
        headers={"Authorization":f"Bearer {auth_token}"}
    )

    response = client.delete(
        "/votes/1/vote",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 204

def test_vote_without_token(client, sample_data):
    response = client.post(
        "/votes/1/vote"
    )

    assert response.status_code == 401

def test_replicated_vote(client,auth_token, sample_data):
    client.post(
            "/votes/1/vote",
            headers={"Authorization":f"Bearer {auth_token}"}
        )
    response =client.post(
            "/votes/1/vote",
            headers={"Authorization":f"Bearer {auth_token}"}
        )

    assert response.status_code == 409
def test_unvote_empty(client,auth_token, sample_data):
    response = client.delete(
        "/votes/1/vote",
        headers={"Authorization" : f"Bearer {auth_token}"}
    )
    assert response.status_code == 404

def test_get_vote_by_book(client, auth_token, sample_data):
    client.post(
                "/votes/1/vote",
                headers={"Authorization":f"Bearer {auth_token}"}
            )
    for i in range(2, 4):   # user2, user3
        client.post("/users/create", json={
            "username": f"user{i}",
            "email": f"user{i}@gmail.com",
            "password": "testpass123",
        })
        login = client.post("/users/login", data={
            "username": f"user{i}",
            "password": "testpass123",
        })
        token = login.json()["access_token"]

        client.post(
            "/votes/1/vote",
            headers={"Authorization": f"Bearer {token}"},
        )

    response = client.get(
        "/votes/1/vote",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    assert response.json()["vote_count"] == 3

