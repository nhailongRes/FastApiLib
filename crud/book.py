from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.book import BookCreate
from exceptions import ValidationError
import model


def create_book(book: BookCreate, db: Session):
    db_book = model.Book(**book.model_dump())
    db.add(db_book)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValidationError("Author does not exist")
    db.refresh(db_book)
    return db_book

def get_books_with_author(author_id: int, db: Session):
    
    results =   db.query(model.Book, model.Author.name,model.Author.id).join(model.Author).filter(model.Author.id == author_id).all()

    return [
        {
            "id": book.id,
            "title": book.title,
            "published_year":book.published_year,
            "author_name": author_name,
            "author_id": a_id
        }
        for book, author_name, a_id in results
    ]


def get_all_books_with_authors_name(db: Session):
    results = db.query(model.Book, model.Author.name).join(model.Author).all()
    return [
        {"id": book.id, "title": book.title, "published_year": book.published_year,
         "author_id": book.author_id, "author_name": author_name}
        for book, author_name in results
    ]
def get_book_by_author_id_and_year(year:int,author_id:int, db:Session ):
    results = db.query(model.Book.title, model.Book.published_year, model.Book.author_id).filter(model.Book.author_id == author_id
                                                                                                 ,model.Book.published_year > year ).all()
    return [
        {
            "book_title" : book_title,
            "published_year" : published_year,
            "author_id" : author_id
        }
        for book_title, published_year, author_id in results
    
    ]
def get_book_by_ids(bookids:list[int], db:Session ):
    books = db.query(model.Book).filter(model.Book.id.in_(bookids)).all()
    return books
def get_book_after_year(year:int, db:Session):
    results = db.query(model.Book.published_year, model.Book.title).filter(model.Book.published_year > year).all()
    return [
        {
            "published_year": published_year,
            "book_title" : book_title
        }
        for published_year, book_title in results
    ]


def get_book_with_voters (book_id:int, db:Session):
    books = db.query(model.Book.title, model.User.username).join(model.Vote, model.Book.id == model.Vote.book_id).join(model.User, model.Vote.user_id == model.User.id).filter(model.Book.id == book_id).all()
    return[
        {
            "book_title":book_title,
            "user_vote":username
        }
        for book_title, username in books
    ]