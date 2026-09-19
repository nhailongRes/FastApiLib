from model import Book,Author
def test_create_book(client,auth_token,example_author):
    response = client.post(
        "/books/",
        json={
            "title":"Nhung Nguoi Khon Kho",
            "author_id":example_author.id,
            "published_year":2000
        }
        ,
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201

def test_create_book_with_wrong_authorid(client,auth_token):
    response = client.post(
            "/books/",
            json={
                "title":"Nhung Nguoi Khon Kho",
                "author_id":3,
                "published_year":2000
            }
            ,
            headers={"Authorization": f"Bearer {auth_token}"}
        )
    assert response.status_code == 400

def test_get_all_book_with_author_name(client,auth_token,sample_data):

    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200


def test_get_books_after_year(client,auth_token,sample_data):
    response = client.get(
        "books/after-year/2000",
        headers={"Authorization":f"Bearer {auth_token}"}
    )

    assert response.status_code == 200

    data = response.json()

    result = {}

    for book in data:
        year = book["published_year"]
        result.setdefault(year,[]).append(book["book_title"])


    assert "Nhung Ke Xuat Chung" in result[2025]