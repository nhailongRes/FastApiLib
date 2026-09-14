from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
from security import SECRET_KEY, ALGORITHM
from exceptions import NotFoundError, ForbiddenError
import model
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise NotFoundError("Invalid token")

    except JWTError:
        raise NotFoundError("Invalid token")

    user = db.query(model.User).filter(model.User.id == int(user_id)).first()
    if not user:
        raise NotFoundError("User not found")

    return user

def required_admin(current_user:model.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise ForbiddenError("Required admin access")
    return current_user