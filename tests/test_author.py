from model import Author,Book

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

def test_search_author_by_name(client, auth_token, db_session):
    db_session.add_all([
            Author(name="Eva", country="Spain"),
            Author(name="Hai", country="Spain"),
            Author(name = "Hai Long", country = "Vietnam")
        ])
    db_session.commit()


    response = client.get (
        "/authors/search", params={'keyword': "Hai"}
        ,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200

    data = response.json()
    names = [a["name"] for a in data]
    assert "Hai Long" in names
    assert "Hai" in names

def test_update_author_name(client, auth_token, db_session):
    authors = [
        Author(name="Nguyen Nhat Anh", country="Vietnam"),
        Author(name="Nguyen Du", country="Vietnam"),
        Author(name="Haruki Murakami", country="Japan"),
        Author(name="Ernest Hemingway", country="USA"),
    ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    response = client.patch(
        "/authors/1",
        json={
            "name":"Nguyen Hai Long"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["country"] == "Vietnam"
    assert data["name"] == "Nguyen Hai Long"

def test_update_author_with_empty_string(client, auth_token, db_session):
    authors = [
            Author(name="Nguyen Nhat Anh", country="Vietnam"),
            Author(name="Nguyen Du", country="Vietnam"),
            Author(name="Haruki Murakami", country="Japan"),
            Author(name="Ernest Hemingway", country="USA"),
        ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)


    response = client.patch(
        "/authors/1",
        json={
            "name":" "
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
def test_update_long_author_name(client, auth_token, db_session):
    authors = [
                Author(name="Nguyen Nhat Anh", country="Vietnam"),
                Author(name="Nguyen Du", country="Vietnam"),
                Author(name="Haruki Murakami", country="Japan"),
                Author(name="Ernest Hemingway", country="USA"),
            ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    response = client.patch(
        "/authors/2",
        json={
            "name":"aaaaajkahsdfjshdfjkhsdjkfhsjkdfjhsdkjfhskjdfhkjsdhfkjskdhfkjshdfkjsdhfjksdhfjksdf"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 400

def test_update_unexisted_author(client, auth_token, db_session):
    authors = [
                    Author(name="Nguyen Nhat Anh", country="Vietnam"),
                    Author(name="Nguyen Du", country="Vietnam"),
                    Author(name="Haruki Murakami", country="Japan"),
                    Author(name="Ernest Hemingway", country="USA"),
                ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    response = client.patch(
        "/authors/5",
        json={
            "name":"Hai Long"
        },
        headers={"Authorization":f"Bearer {auth_token}"}
    )

    assert response.status_code == 404

def test_delete_author(client, auth_token, db_session):
    authors = [
                        Author(name="Nguyen Nhat Anh", country="Vietnam"),
                        Author(name="Nguyen Du", country="Vietnam"),
                        Author(name="Haruki Murakami", country="Japan"),
                        Author(name="Ernest Hemingway", country="USA"),
                    ]

    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    response = client.delete(
        "authors/1",
        headers={"Authorization":f"Bearer {auth_token}"}
    )
    assert response.status_code == 204
def test_delete_unknown_author(client, auth_token, db_session):
    authors = [
                            Author(name="Nguyen Nhat Anh", country="Vietnam"),
                            Author(name="Nguyen Du", country="Vietnam"),
                            Author(name="Haruki Murakami", country="Japan"),
                            Author(name="Ernest Hemingway", country="USA"),
                        ]
    db_session.add_all(authors)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    response = client.delete(
        "authors/5",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 404

def test_book_count_per_author(client, auth_token, db_session):
    authors = [
                            Author(name="Nguyen Nhat Anh", country="Vietnam"),
                            Author(name="Nguyen Du", country="Vietnam"),
                            Author(name="Haruki Murakami", country="Japan"),
                            Author(name="Ernest Hemingway", country="USA"),
                        ]

    books = [
    Book(title="Nha Gia Kim", author=authors[0], published_year=2024),
    Book(title="Nhung Ke Xuat Chung", author=authors[0], published_year=2025),
    Book(title="Hard Things About Hard Thing", author=authors[1], published_year=2000),
    Book(title="Tu Tot Den Vi Dai", author=authors[2], published_year=2000),
            ]

    db_session.add_all(authors)
    db_session.add_all(books)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)

    for b in books:
        db_session.refresh(b)

    response = client.get(
        "authors/books",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()


    result = {item["author_name"]: item["book_count"] for item in data}
    assert result["Nguyen Nhat Anh"] == 2
    assert result["Nguyen Du"] == 1
    assert result["Haruki Murakami"] == 1

def test_get_profilic_authors(client, auth_token, db_session):
    authors = [
                                Author(name="Nguyen Nhat Anh", country="Vietnam"),
                                Author(name="Nguyen Du", country="Vietnam"),
                                Author(name="Haruki Murakami", country="Japan"),
                                Author(name="Ernest Hemingway", country="USA"),
    ]
    books = [
        Book(title="Nha Gia Kim", author=authors[0], published_year=2024),
        Book(title="Nhung Ke Xuat Chung", author=authors[0], published_year=2025),
        Book(title="Hard Things About Hard Thing", author=authors[1], published_year=2000),
        Book(title="Tu Tot Den Vi Dai", author=authors[2], published_year=2000),
        Book(title = "Zero To One", author=authors[0], published_year = 2015)
                ]
        

    db_session.add_all(authors)
    db_session.add_all(books)
    db_session.commit()
    for a in authors:
        db_session.refresh(a)
    
    for b in books:
        db_session.refresh(b)


    response = client.get(
        "authors/prolific",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200

    data = response.json()
    result = {item["author_name"] : item["book_count"] for item in data}
    assert result["Nguyen Nhat Anh"] == 3


def test_get_author_book_counts_including_zero(client, auth_token, db_session):
    authors = [
                                    Author(name="Nguyen Nhat Anh", country="Vietnam"),
                                    Author(name="Nguyen Du", country="Vietnam"),
                                    Author(name="Haruki Murakami", country="Japan"),
                                    Author(name="Ernest Hemingway", country="USA"),
                                    Author(name = "Le Quang Huy", country = "Vietnam"),
                                    Author(name = "Nguyen Tan Dung", country = "Vietnam")
        ]
    books = [
            Book(title="Nha Gia Kim", author=authors[0], published_year=2024),
            Book(title="Nhung Ke Xuat Chung", author=authors[0], published_year=2025),
            Book(title="Hard Things About Hard Thing", author=authors[1], published_year=2000),
            Book(title="Tu Tot Den Vi Dai", author=authors[2], published_year=2000),
            Book(title = "Zero To One", author=authors[0], published_year = 2015)
            ]


    db_session.add_all(authors)
    db_session.add_all(books)
    db_session.commit()
    for a in authors :
        db_session.refresh(a)
    for b in books:
        db_session.refresh(b)

    response = client.get(
        "authors/books-including-zero",
        headers={"Authorization" : f"Bearer {auth_token}"}
    )

    assert response.status_code == 200

    data = response.json()
    result = {item["author_name"] : item["book_count"] for item in data}
    assert result["Nguyen Nhat Anh"] == 3
    assert result["Haruki Murakami"] == 1
    assert result["Le Quang Huy"] == 0
    assert result["Nguyen Tan Dung"] == 0
