from model import Author

def test_create_author(client, auth_token):
    response = client.post(
        "/authors",
        json={"name": "Eva", "country": "Spain"},
        headers={"Authorization": f"Bearer {auth_token}"}    # <-- THÊM TOKEN VÀO HEADER
    )
    assert response.status_code == 201

def test_create_author_without_token(client):
    response = client.post(
        "/authors",
        json = {
            "name":"Hai",
            "country":"Vietnam"
        }
    )
    assert response.status_code == 401

def test_create_author_missingfield(client,auth_token):
    response = client.post(
        "/authors",
        json = {
            "name":"Ray"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 422
def test_get_all_authors(client, auth_token):
    # 1. Tự seed 1 author
    create_resp = client.post(
        "/authors",
        json={"name": "Eva", "country": "Spain"},
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert create_resp.status_code == 201

    response = client.get(
        "/authors",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Eva"
    assert data[0]["country"] == "Spain"


def test_get_author_with_id(client, auth_token):
    create_resp = client.post(
            "/authors",
            json={"name": "Eva", "country": "Spain"},
            headers={"Authorization": f"Bearer {auth_token}"},
    )
    response = client.get(
        "/authors/1",
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == 1
    assert data["name"] == "Eva"
    assert data["country"] == "Spain"



def test_get_author_with_wrong_id(client,auth_token):
    create_resp = client.post(
        "/authors",
        json = {
            "name":"Eva",
            "country":"Spain"
        }
        ,headers={"Authorization":f"Bearer {auth_token}"}
    )

    assert create_resp.status_code == 201

    response = client.get(
            "/authors/2",
            headers={"Authorization":f"Bearer {auth_token}"}
        )

    assert response.status_code == 404

def test_get_author_by_country(client, auth_token, db_session):
    db_session.add_all([
        Author(name="Eva", country="Spain"),
        Author(name="Hai", country="Spain"),
    ])
    db_session.commit()

    response = client.get(
        "/authors/country/Spain",
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert len(data) == 2
    countries = [a["author_country"] for a in data]
    assert countries == ["Spain", "Spain"]
    names = {a["author_name"] for a in data}
    assert names == {"Eva", "Hai"}