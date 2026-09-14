from pydantic import BaseModel
class AuthorCreate(BaseModel):
    name: str
    country:str
class AuthorOut(BaseModel):
    id: int
    name: str
    country: str
    class Config:
        from_attributes = True
class AuthorByCountry(BaseModel):
    author_name: str
    author_country: str
class ProlificAuthor(BaseModel):
    author_name: str
    book_count: int
class UpdateAuthorName(BaseModel):
    name: str