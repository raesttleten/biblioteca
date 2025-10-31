from typing import List, Optional
from pydantic import BaseModel, Field, validator
import re

ISBN_REGEX = re.compile(r"^[0-9\-]{8,20}$")  # simple pattern: digits and dashes

class AuthorCreate(BaseModel):
    name: str = Field(..., min_length=1)
    country: Optional[str] = None
    birth_year: Optional[int] = None

class AuthorRead(AuthorCreate):
    id: int
    books: List["BookReadSimple"] = []

class BookCreate(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    copies: int = Field(1, ge=0)
    author_ids: Optional[List[int]] = []

    @validator("isbn")
    def isbn_valid(cls, v):
        if not ISBN_REGEX.match(v):
            raise ValueError("ISBN inválido (usar sólo dígitos y guiones, longitud razonable)")
        return v

class BookReadSimple(BaseModel):
    id: int
    title: str
    isbn: str

class BookRead(BookReadSimple):
    publication_year: Optional[int] = None
    copies: int
    authors: List[AuthorRead] = []
