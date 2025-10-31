from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Author, AuthorCreate, AuthorRead, AuthorUpdate
from app import crud

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=AuthorRead, summary="Crear un nuevo autor")
def crear_autor(autor: AuthorCreate, session: Session = Depends(get_session)):
    nuevo_autor = Author.from_orm(autor)
    return crud.crear_autor(session, nuevo_autor)

@router.get("/", response_model=list[AuthorRead], summary="Listar todos los autores")
def listar_autores(session: Session = Depends(get_session)):
    return crud.listar_autores(session)

@router.get("/{autor_id}", response_model=AuthorRead, summary="Obtener un autor por ID")
def obtener_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = crud.obtener_autor(session, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

@router.put("/{autor_id}", response_model=AuthorRead, summary="Actualizar un autor")
def actualizar_autor(autor_id: int, autor_actualizado: AuthorUpdate, session: Session = Depends(get_session)):
    autor = crud.obtener_autor(session, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return crud.actualizar_autor(session, autor, autor_actualizado.dict(exclude_unset=True))

@router.delete("/{autor_id}", summary="Eliminar un autor")
def eliminar_autor(autor_id: int, session: Session = Depends(get_session)):
    autor = crud.obtener_autor(session, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    crud.eliminar_autor(session, autor)
    return {"mensaje": "Autor eliminado exitosamente"}