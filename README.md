# Sistema de Gestión de Libros y Autores

Este proyecto es una API desarrollada con **FastAPI** y **SQLModel**, diseñada para administrar información sobre **libros y autores**, aplicando reglas de negocio reales para garantizar la consistencia e integridad de los datos.

La API permite registrar, consultar, actualizar y eliminar tanto autores como libros, con control lógico sobre las relaciones entre ellos.

---

## Tecnologías utilizadas
- **Python 3.10+**
- **FastAPI** (framework principal)
- **SQLModel** (ORM y modelo de base de datos)
- **Uvicorn** (servidor ASGI)
- **SQLite** (base de datos liviana por defecto)
- **Pydantic** (validación de datos)

---

## Estructura del proyecto

proyecto_biblioteca/

┣ main.py

┣ models.py

┣ schemas.py

┣ crud.py

┣ README.md

┗ requeriments.txt

┗ routers/autores, /libros

- `main.py`: Configura FastAPI y las rutas principales.  
- `models.py`: Define las tablas y relaciones (Libro, Autor).  
- `schemas.py`: Define validaciones y estructuras Pydantic.  
- `crud.py`: Contiene toda la lógica de negocio (5 reglas).  

---
### Clonar el repositorio
```bash
git clone https://github.com/raesttleten/biblioteca.git
cd biblioteca

instalar dependencias:
pip install fastapi uvicorn sqlmodel
uvicorn app.main:app --reload
URL: http://127.0.0.1:8000/docs



