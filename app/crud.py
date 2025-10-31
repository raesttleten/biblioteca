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

def get_author(session: Session, author_id: int) -> Author:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Autor no encontrado")
    return author

def update_author(session: Session, author_id: int, author_in: AuthorCreate) -> Author:
    author = get_author(session, author_id)
    author.name = author_in.name
    author.country = author_in.country
    author.birth_year = author_in.birth_year
    session.add(author)
    session.commit()
    session.refresh(author)
    return author
