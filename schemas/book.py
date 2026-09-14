from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author_id: int
    published_year: int


class BookUpdate(BaseModel):
    title: str | None = None
    published_year: int | None = None
    author_id: int | None = None


class BookOut(BaseModel):
    id: int
    title: str
    author_id: int
    published_year: int
    class Config:
        from_attributes = True
class BookWithAuthorName(BaseModel):
    id: int
    title: str
    published_year: int
    author_name: str
    author_id: int
class BookAfterYear(BaseModel):
    published_year: int
    book_title: str


class BookByAuthorIdAndYear(BaseModel):
    book_title: str
    published_year: int
    author_id: int


class BookCountPerAuthor(BaseModel):
    author_name: str
    book_count: int


class BookWithVoter(BaseModel):
    book_title: str
    user_vote: str