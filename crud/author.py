from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.author import AuthorCreate
from exceptions import NotFoundError, ValidationError
import model
from sqlalchemy.exc import SQLAlchemyError
from exceptions import ConflictError, NotFoundError, ValidationError,DatabaseError

def create_author(author: AuthorCreate, db: Session):
    db_author = model.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_all_authors(db: Session):
    return db.query(model.Author).all()


def get_author_by_id(id: int, db: Session):
    author = db.query(model.Author).filter(model.Author.id == id).first()
    if not author:
        raise NotFoundError("Author not found")
    return author


def get_author_by_country(country: str, db: Session):
    results = db.query(model.Author.name, model.Author.country).filter(
        func.lower(model.Author.country) == country.lower()
    ).all()
    return [{"author_name": n, "author_country": c} for n, c in results]
def search_author_by_name(keyword:str, db:Session):
    authors = db.query(model.Author).filter(model.Author.name.like(f"%{keyword}%")).all()
    return authors

def get_author_with_books(author_id: int, db: Session):
    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise NotFoundError(detail="Author not found")
    return author.books
def count_books_per_author(db:Session):
    books =  db.query(model.Author.name, func.count(model.Book.id)).join(model.Book).group_by(model.Author.name).all()
    return[
        {
            "author_name":author_name,
            "book_count":book_count
        }
        for author_name, book_count in books
    ]
def get_prolific_authors(db:Session):
    authors = db.query(model.Author.name.label("Author_having_more_than_2_books"),func.count(model.Book.id)).join(model.Book).group_by(model.Author.name).having(func.count(model.Book.id)>2).all()
    return[
        {
            "author_name":author_name,
            "book_count":book_count
        }
        for author_name,book_count in authors
    ]
def get_author_book_counts_including_zero(db: Session):
    results = db.query(model.Author.name, func.count(model.Book.id).label("book_count")).outerjoin(model.Book).group_by(model.Author.name).all()
    return[
        {
            "author_name":author_name,
            "book_count":book_count
        }
        for author_name, book_count in results
    ]
def update_author_name(author_id: int, name: str, db: Session):
    if not name or not name.strip():
        raise ValidationError(detail="Name cannot be empty")
    if len(name) > 30:
        raise ValidationError(detail="Name too long")

    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise NotFoundError(detail="Author not found")

    author.name = name
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))
    db.refresh(author)
    return author
def delete_author(author_id:int, db:Session):
    author = db.query(model.Author).filter(model.Author.id == author_id).first()
    if not author:
        raise NotFoundError(detail="author not found")
    try:
        db.delete(author)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

# ... CÁC HÀM AUTHOR KHÁC (search, update, delete, count, prolific...)