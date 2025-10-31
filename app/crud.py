import datetime

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

def create_book(session: Session, book_in: BookCreate) -> Book:
    # 🔸 Regla 1: ISBN único
    existing = session.exec(select(Book).where(Book.isbn == book_in.isbn)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ISBN ya existe")

    # 🔸 Regla 4: Validar año de publicación (no puede ser futuro)
    current_year = datetime.now().year
    if book_in.publication_year and book_in.publication_year > current_year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Año de publicación inválido ({book_in.publication_year}), no puede ser mayor que {current_year}"
        )

    book = Book(
        title=book_in.title,
        isbn=book_in.isbn,
        publication_year=book_in.publication_year,
        copies=book_in.copies
    )

    # Asociar autores (Regla 5)
    if book_in.author_ids:
        for aid in book_in.author_ids:
            author = session.get(Author, aid)
            if not author:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Autor {aid} no existe")

            # 🔸 Regla 5: Límite de 10 libros por autor
            if len(author.books) >= 10:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El autor '{author.name}' ya tiene 10 libros registrados. No se pueden asignar más."
                )

            book.authors.append(author)

    # 🔸 Regla 2: Copias no negativas (validación doble)
    if book.copies < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Copias no puede ser negativo")

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def get_book(session, book_id):
    pass


def update_book(session: Session, book_id: int, book_in: BookCreate) -> Book:
    book = get_book(session, book_id)

    # 🔸 Regla 4: año no puede ser futuro
    current_year = datetime.now().year
    if book_in.publication_year and book_in.publication_year > current_year:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Año de publicación inválido ({book_in.publication_year}), no puede ser mayor que {current_year}"
        )

    # 🔸 Regla 1: ISBN único (si se cambia)
    if book.isbn != book_in.isbn:
        existing = session.exec(select(Book).where(Book.isbn == book_in.isbn)).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ISBN ya existe")

    # 🔸 Regla 2: Copias no negativas
    if book_in.copies < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Copias no puede ser negativo")

    book.title = book_in.title
    book.isbn = book_in.isbn
    book.publication_year = book_in.publication_year
    book.copies = book_in.copies

    # Reasociar autores si se envían
    if book_in.author_ids is not None:
        book.authors.clear()
        for aid in book_in.author_ids:
            author = session.get(Author, aid)
            if not author:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Autor {aid} no existe")

            # 🔸 Regla 5: máximo 10 libros por autor
            if len(author.books) >= 10 and book not in author.books:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El autor '{author.name}' ya tiene 10 libros registrados. No se pueden asignar más."
                )
            book.authors.append(author)

    session.add(book)
    session.commit()
    session.refresh(book)
    return book