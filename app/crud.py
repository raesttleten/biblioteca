from sqlmodel import select, Session
from fastapi import HTTPException, status
from typing import List
from .models import Author, Book
from .schemas import AuthorCreate, BookCreate

def create_author(session: Session, author_in: AuthorCreate) -> Author:
    author = Author.from_orm(author_in)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author
def list_authors(session: Session, country: str = None) -> List[Author]:
    q = select(Author)
    if country:
        q = q.where(Author.country == country)
    return session.exec(q).all()