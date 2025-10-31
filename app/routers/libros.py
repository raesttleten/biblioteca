from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models import Book, BookCreate, BookRead, BookUpdate
from app import crud

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
    responses={404: {"description": "No encontrado"}},
)

@router.post("/", response_model=BookRead, summary="Crear un nuevo libro")
def crear_libro(libro: BookCreate, session: Session = Depends(get_session)):
    nuevo_libro = Book.from_orm(libro)
    return crud.crear_libro(session, nuevo_libro)

@router.get("/", response_model=list[BookRead], summary="Listar todos los libros")
def listar_libros(session: Session = Depends(get_session)):
    return crud.listar_libros(session)

@router.get("/{libro_id}", response_model=BookRead, summary="Obtener un libro por ID")
def obtener_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = crud.obtener_libro(session, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@router.put("/{libro_id}", response_model=BookRead, summary="Actualizar un libro")
def actualizar_libro(libro_id: int, libro_actualizado: BookUpdate, session: Session = Depends(get_session)):
    libro = crud.obtener_libro(session, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return crud.actualizar_libro(session, libro, libro_actualizado.dict(exclude_unset=True))

@router.delete("/{libro_id}", summary="Eliminar un libro")
def eliminar_libro(libro_id: int, session: Session = Depends(get_session)):
    libro = crud.obtener_libro(session, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    crud.eliminar_libro(session, libro)
    return {"mensaje": "Libro eliminado exitosamente"}