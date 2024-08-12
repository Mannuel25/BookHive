from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import date

class BookCreateSchema(BaseModel):
    title: str
    author: str
    publication_date: date
    isbn: str
    tag: Optional[str] = 'admin'


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[date] = None
    isbn: Optional[str] = None
    tag: Optional[str] = None


class BookResponseSchema(BaseModel):
    id: int
    title: str
    author: str
    publication_date: date
    isbn: str
    tag: str
    date_created: str
    date_updated: str

