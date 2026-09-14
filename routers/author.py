from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.author import AuthorCreate, AuthorOut, AuthorByCountry, ProlificAuthor, UpdateAuthorName
from crud.author import (
    create_author, get_all_authors, get_author_by_id, get_author_by_country,
    search_author_by_name, update_author_name, delete_author,
    count_books_per_author, get_prolific_authors, get_author_book_counts_including_zero
)
import model
from routers.protected import get_current_user

router = APIRouter(prefix="/authors", tags=["Authors"])    


@router.post("", response_model=AuthorOut, status_code=201)
def create_author_endpoint(author: AuthorCreate, conn: Session = Depends(get_db),current_user: model.User = Depends(get_current_user)):
    return create_author(author, conn)
@router.get("", response_model=list[AuthorOut])
def get_authors_endpoint(conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return get_all_authors(conn)
@router.get("/country/{country}", response_model=list[AuthorByCountry])
def get_authors_by_country_endpoint(country: str, conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return get_author_by_country(country, conn)
@router.get("/{author_id}", response_model=AuthorOut)
def get_author_endpoint(author_id: int, conn: Session = Depends(get_db),current_user:model.User = Depends(get_current_user)):
    return get_author_by_id(author_id, conn)