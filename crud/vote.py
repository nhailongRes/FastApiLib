from sqlalchemy.orm import Session
import model
from exceptions import ConflictError,NotFoundError
from sqlalchemy import func

def create_vote(user_id:int, book_id: int ,db:Session) -> model.Vote:
    existing = db.query(model.Vote).filter(model.Vote.book_id == book_id, model.Vote.user_id == user_id).first()
    if existing:
        raise ConflictError("vote already existed")


    new_vote = model.Vote(user_id= user_id, book_id = book_id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return new_vote

def unvote(user_id:int, book_id:int, db:Session):
    existing = db.query(model.Vote).filter(model.Vote.book_id == book_id, model.Vote.user_id == user_id).first()
    if not existing:
        raise NotFoundError("Vote not found!")

    db.delete(existing)
    db.commit()

def get_book_vote_count(book_id: int, db: Session):
    count = db.query(func.count(model.Vote.user_id)).filter(model.Vote.book_id == book_id).scalar()
    return {"book_id": book_id, "vote_count": count}
