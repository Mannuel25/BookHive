from bookhiveConfig.utils import AuthSetupTestCase
from .models import Book


class BookTests(AuthSetupTestCase):
    """
    A test case class for handling book-related API tests.

    This class inherits from AuthSetupTestCase. It includes various test cases for CRUD operations on the BookHive Books API.
    """

    def setUp(self):
        self.authenticate()
        self.book_data = {
            "title": "Sample Book",
            "author": "Author Name",
            "publication_date": "2024-01-01",
            "isbn": "1234567890123",
            "owner": self.user,
            "tag": "custom",
        }
        self.book_id = Book.objects.create(**self.book_data).id

    def test_book_list(self):
        response = self.client.get('/api/book_mgt/books')
        self.assertEqual(response.status_code, 200)

    def test_book_post(self):
        response = self.client.post('/api/book_mgt/books', data={
            "title": "New Book",
            "author": "New Author",
            "publication_date": "2024-02-01",
            "isbn": "9876543210987",
            "tag": "admin",
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_book_get(self):
        url = f'/api/book_mgt/books/{self.book_id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_book_patch(self):
        url = f'/api/book_mgt/books/{self.book_id}'
        response = self.client.patch(url, data={
            "title": "Updated Book Title",
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_book_put(self):
        response = self.client.post('/api/book_mgt/books', data={
            "title": "Original Title",
            "author": "Original Author",
            "publication_date": "2024-01-01",
            "isbn": "1234567890123",
            "tag": "admin",
        }, format='json')
        book_id = response.json().get('data').get('id')
        response = self.client.put(f'/api/book_mgt/books/{book_id}', data={
            "title": "Updated Title",
            "author": "Updated Author",
            "publication_date": "2024-02-01",
            "isbn": "9876543210987",
            "tag": "admin",
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_book_delete(self):
        url = f'/api/book_mgt/books/{self.book_id}'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
