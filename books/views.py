from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db import transaction
from typing import List
from .models import Book
from .schemas import *
from bookhiveConfig.utils import get_api, CustomResponse


api = get_api(
    title="BookHive Books API",
    description="This documentation provides endpoints for managing all books.",
    version="1.0.1"
)


def return_book_data(book):
    # this function returns the details of the passed-in book
    return BookResponseSchema(
        id=book.id,
        title=book.title,
        author=book.author,
        publication_date=book.publication_date,
        isbn=book.isbn,
        tag=book.tag,
        date_created=book.date_created.isoformat(),
        date_updated=book.date_updated.isoformat()
    ).dict()


@api.post("/books", response=BookResponseSchema)
@transaction.atomic
def create_book(request, data: BookCreateSchema):
    try:
        # ensure a user is authenticated before creating a book
        if not request.user.is_authenticated:
            return CustomResponse.failed(message="Kindly login to create a book.", status=403)

        book = Book.objects.create(
            title=data.title,
            author=data.author,
            publication_date=data.publication_date,
            isbn=data.isbn,
            tag=data.tag,
            owner=request.user if data.tag != 'admin' else None
        )
        return CustomResponse.success(data=return_book_data(book), message="Book created successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.get("/books", response=List[BookResponseSchema])
def get_all_books(request, page=1, size=10, id=None, title=None, author=None, tag=None):
    try:
        # show recently added books first
        queryset = Book.objects.all().order_by('-id')
        # apply filters dynamically based on the id, title, author, tag
        if id:
            queryset = queryset.filter(id=id)
        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__icontains=author)
        if tag:
            queryset = queryset.filter(tag=tag)

        paginator = Paginator(queryset, size)
        paginated_books = paginator.get_page(page)

        books = [return_book_data(book) for book in paginated_books.object_list]

        return CustomResponse.success(
            data={
                "books": books,
                "page": page,
                "size": size,
                "total_pages": paginator.num_pages,
                "total_books": paginator.count
            },
            message="Books retrieved successfully"
        )
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.get("/books/{book_id}", response=BookResponseSchema)
def get_book_by_id(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        return CustomResponse.success(data=return_book_data(book), message="Book retrieved successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.patch("/books/{book_id}", response=BookResponseSchema)
def update_book(request, book_id, data: BookUpdateSchema):
    try:
        book = get_object_or_404(Book, id=book_id)
        # check if the logged-in "user" is the owner of the book or if the book is an admin book
        if request.user.user_type == "user":
            if book.owner != request.user and book.tag == 'admin':
                return CustomResponse.failed(message="You do not have the permission to update this book.", status=403)
        for attr, value in data.dict().items():
            if value is not None:
                setattr(book, attr, value)
        book.save()
        return CustomResponse.success(data=return_book_data(book), message="Book updated successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.put("/books/{book_id}", response=BookResponseSchema)
def replace_book(request, book_id, data: BookUpdateSchema):
    try:
        book = get_object_or_404(Book, id=book_id)
        # Check if the logged-in "user" is the owner of the book or if the book is an admin book
        if request.user.user_type == "user":
            if book.owner != request.user and book.tag == 'admin':
                return CustomResponse.failed(message="You do not have the permission to replace this book.", status=403)
        book.title = data.title if data.title else book.title
        book.author = data.author if data.author else book.author
        book.publication_date = data.publication_date if data.publication_date else book.publication_date
        book.isbn = data.isbn if data.isbn else book.isbn
        book.tag = data.tag if data.tag else book.tag
        book.save()
        return CustomResponse.success(data=return_book_data(book), message="Book updated successfully")
    except Exception as e:
        return CustomResponse.failed(message=str(e))


@api.delete("/books/{book_id}", response=dict)
def delete_book(request, book_id):
    try:
        book = get_object_or_404(Book, id=book_id)
        # Check if the request user is the owner of the book or if the book is an admin book
        if request.user.user_type == "user":
            if book.owner != request.user and book.tag == 'admin':
                return CustomResponse.failed(message="You do not have the permission to delete this book.", status=403)
        book.delete()
        return CustomResponse.success(message="Book deleted successfully", status=204)
    except Exception as e:
        return CustomResponse.failed(message=str(e))


