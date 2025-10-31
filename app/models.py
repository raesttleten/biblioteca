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