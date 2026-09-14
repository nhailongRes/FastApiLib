from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.book import BookCreate, BookOut, BookWithAuthorName, BookAfterYear,BookWithVoter
from crud.book import create_book, get_all_books_with_authors_name, get_book_after_year,get_book_with_voters
from routers.protected import get_current_user
import model
router = APIRouter(prefix="/books", tags=["Books"])


@router.post("", response_model=BookOut, status_code=201)
def create_book_endpoint(book: BookCreate, conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return create_book(book, conn)


@router.get("", response_model=list[BookWithAuthorName])
def get_all_books_endpoint(conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return get_all_books_with_authors_name(conn)


@router.get("/after-year/{year}", response_model=list[BookAfterYear])
def get_books_after_year_endpoint(year: int, conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return get_book_after_year(year, conn)
@router.get("/{book_id}/voters", response_model=list[BookWithVoter])
def get_book_with_voters_endpoint(
    book_id: int,
    conn: Session = Depends(get_db),
    current_user: model.User = Depends(get_current_user)
):
    return get_book_with_voters(book_id=book_id, db=conn)
