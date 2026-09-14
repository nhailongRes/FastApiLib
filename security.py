import os
from dotenv import load_dotenv
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from jose import jwt

password_hash = PasswordHash.recommended()
load_dotenv() 

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data:dict, expire_delta:timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expire_delta
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(claims=to_encode,key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt