from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)

class Base(DeclarativeBase):
    pass
def get_db():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()