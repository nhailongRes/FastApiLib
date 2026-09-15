from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
import os
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(bind = engine)

class Base(DeclarativeBase):
    pass
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()