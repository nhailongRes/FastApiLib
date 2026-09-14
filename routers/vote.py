from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from routers.protected import get_current_user
from crud.vote import create_vote, unvote, get_book_vote_count
import model
router = APIRouter(prefix="/votes", tags=["Votes"])

@router.post("/{book_id}/vote", status_code=201)
def vote_book_endpoint(
    book_id:int,
    current_user: model.User = Depends(get_current_user),
    conn : Session = Depends(get_db)
):

    return create_vote(user_id= current_user.id, book_id= book_id,db= conn)

@router.delete("/{book_id}/vote", status_code=204)
def unvote_endpoint(
    book_id:int,
    current_user: model.User = Depends(get_current_user),
    conn: Session = Depends(get_db)
):
    return unvote(user_id=current_user.id, book_id= book_id, db= conn)
@router.get("/{book_id}/vote")
def get_vote_by_book(
    book_id:int,
    conn: Session = Depends(get_db)
):
    return get_book_vote_count(book_id=book_id, db=conn)