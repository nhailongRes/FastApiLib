from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserOut
from crud.user import create_user, get_user_by_id,authenticate_user,get_all_user
from fastapi.security import OAuth2PasswordRequestForm
from security import create_access_token
from routers.protected import get_current_user,required_admin
import model

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create", response_model=UserOut, status_code=201)
def create_user_endpoint(user: UserCreate, conn: Session = Depends(get_db)):
    return create_user(user, conn)

@router.get("/all",response_model=list[UserOut])
def get_all_users_endpoint(conn:Session = Depends(get_db),current_user:model.User = Depends(required_admin)):
    return get_all_user(conn)

@router.post("/login")
def login(formdata:OAuth2PasswordRequestForm = Depends(),conn:Session = Depends(get_db)):
    user = authenticate_user(formdata.username, formdata.password,conn)
    access_token = create_access_token(data={"sub":str(user.id)})
    return{"access_token":access_token, "token_type":"bearer"}

@router.get("/me", response_model=UserOut)
def get_my_profile(current_user: model.User = Depends(get_current_user)):
    return current_user
@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: int, conn: Session = Depends(get_db),current_user:model.User = Depends(required_admin)):
    return get_user_by_id(user_id, conn)
