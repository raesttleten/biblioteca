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

def delete_author(session: Session, author_id: int, cascade_books: bool = False) -> None:
    author = get_author(session, author_id)
    if cascade_books:
        # borrar libros que queden sin autores o los que correspondan:
        # enfoque: eliminar autor y si un libro queda sin autores, eliminar ese libro.
        for book in list(author.books):
            book.authors.remove(author)
            if len(book.authors) == 0:
                session.delete(book)
    else:
        for book in list(author.books):
            if author in book.authors:
                book.authors.remove(author)
    session.delete(author)
    session.commit()

    def delete_author(session: Session, author_id: int, cascade_books: bool = False) -> None:
        author = get_author(session, author_id)
        if cascade_books:
            # borrar libros que queden sin autores o los que correspondan:
            # enfoque: eliminar autor y si un libro queda sin autores, eliminar ese libro.
            for book in list(author.books):
                # remove author from book
                book.authors.remove(author)
                if len(book.authors) == 0:
                    session.delete(book)
        else:
            # sólo disociar autor de sus libros (no eliminar libros)
            for book in list(author.books):
                if author in book.authors:
                    book.authors.remove(author)
        session.delete(author)
        session.commit()