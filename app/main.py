from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from .database import create_db_and_tables, get_session, engine
from . import crud, models, schemas

app = FastAPI(title="Sistema de gestión de Biblioteca", version="1.0.0", docs_url="/docs", redoc_url="/redoc")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Authors
@app.post("/autores/", response_model=schemas.AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(author_in: schemas.AuthorCreate, session: Session = Depends(get_session)):
    author = crud.create_author(session, author_in)
    return author

@app.get("/autores/", response_model=List[schemas.AuthorRead])
def list_authors(country: Optional[str] = Query(None), session: Session = Depends(get_session)):
    return crud.list_authors(session, country)

@app.get("/autores/{autor_id}", response_model=schemas.AuthorRead)
def get_author(author_id: int, session: Session = Depends(get_session)):
    return crud.get_author(session, author_id)

@app.put("/autores/{autor_id}", response_model=schemas.AuthorRead)
def update_author(author_id: int, author_in: schemas.AuthorCreate, session: Session = Depends(get_session)):
    return crud.update_author(session, author_id, author_in)

@app.delete("/autores/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, cascade_books: bool = Query(False, description="Si true, elimina libros que queden sin autores"), session: Session = Depends(get_session)):
    crud.delete_author(session, author_id, cascade_books=cascade_books)
    return