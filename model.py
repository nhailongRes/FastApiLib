from sqlalchemy import ForeignKey, String, DateTime,Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime

class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    books: Mapped[list["Book"]] = relationship(back_populates="author")
    country: Mapped[str] = mapped_column(String(30))

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
    published_year : Mapped[int] = mapped_column(Integer)
    votes: Mapped[list["Vote"]] = relationship(back_populates="book")

class User(Base):
    __tablename__ = "Users"
    id:Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    role:Mapped[str] = mapped_column(String(30), default="user")
    votes: Mapped[list["Vote"]] = relationship(back_populates="user")
    

class Vote(Base):
    #In here we gonna user composite prinary key to demonstrate the many to many
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
    user: Mapped["User"] = relationship(back_populates="votes")
    book: Mapped["Book"] = relationship(back_populates="votes")

