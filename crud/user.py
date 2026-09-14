from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.user import UserCreate
from security import hash_password,verify_password
from exceptions import ConflictError, NotFoundError
import model
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError


oauth2_scheme  = OAuth2PasswordBearer(tokenUrl="users/login")

def create_user(user: UserCreate, db: Session):
    existing = db.query(model.User).filter(
        (model.User.username == user.username) | (model.User.email == user.email)
    ).first()
    if existing:
        raise ConflictError("Username or email already exists")

    hashed = hash_password(user.password)
    db_user = model.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("Username or email already exists")
    db.refresh(db_user)
    return db_user


def get_user_by_id(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise NotFoundError("User not found")
    return user


def authenticate_user(username:str,password:str, db:Session):
    user = db.query(model.User).filter(model.User.username == username).first()
    if not user:
        raise NotFoundError("Incorrect username or password")
    if not verify_password(password,user.hashed_password):
        raise NotFoundError("Incorrect username or password")
    return user


def get_all_user(db:Session):
    return db.query(model.User).all()