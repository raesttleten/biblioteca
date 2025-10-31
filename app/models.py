from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship, Column, String, Integer, Table
from datetime import date

# association table (many-to-many)
book_author_link = Table(
    "book_author_link",
    SQLModel.metadata,
    Column("book_id", Integer, primary_key=True),
    Column("author_id", Integer, primary_key=True),
)

class AuthorBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=200)
    country: Optional[str] = Field(None, max_length=100)
    birth_year: Optional[int] = None

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List["Book"] = Relationship(back_populates="authors", link_model=book_author_link)

class BookBase(SQLModel):
    title: str = Field(..., min_length=1, max_length=300)
    isbn: str = Field(
        ...,
        description="ISBN único del libro",
        sa_column=Column(String, unique=True, index=True, nullable=False),
    )
    publication_year: Optional[int] = None
    copies: int = Field(1, ge=0, description="Número de copias disponibles (>=0)")

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    authors: List[Author] = Relationship(back_populates="books", link_model=book_author_link)