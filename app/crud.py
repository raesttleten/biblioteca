from sqlmodel import select, Session
from fastapi import HTTPException, status
from typing import List
from .models import Author, Book
from .schemas import AuthorCreate, BookCreate