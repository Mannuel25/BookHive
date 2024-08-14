

# 📚 BookHive API

## Overview 📋

BookHive is a powerful API designed to simplify the management of your book collection. With this API, you can seamlessly:

- Create, Update, and Retrieve book records 📚
- Filter books based on various attributes 🔍
- Manage user authentication and authorization securely 🔐

## Key Features ⭐
- User Permissions: Users can only modify or delete books that they own. Admins have full access to manage all books, ensuring that each user can only interact with their own records. 🔒
- Advanced Filtering: Easily search and filter books based on title, author, publication date, and more, providing a tailored experience for managing your collection. 🔍
- JWT Authentication: Secure access with JSON Web Tokens (JWT) for user authentication. Refresh tokens and secure login mechanisms keep your data safe. 🔑
Built with Django, Django Ninja, and Pydantic, BookHive leverages PostgreSQL for robust data management and is deployed on Render for seamless scalability. 🚀

## Technologies Used 🛠️

- **Django**: 🕸️ Web framework for building the API.
- **Django Ninja**: ⚡ Fast API framework for Django.
- **Pydantic**: 🔍 Data validation and settings management.
- **PostgreSQL**: 🗄️ Relational database for storing data.
- **Render**: 🌐 Deployment platform for hosting the API.

## Project Setup 🏗️

### Prerequisites

- Python 3.6+
- PostgreSQL
- `pip` (Python package installer)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Mannuel25/bookhive.git
   cd bookhive
   ```

2. **Create a virtual environment**
    ```
    python -m venv .\venv
    ```
3.  **Activate the virtual environment**
    ```
    venv\scripts\activate
    ```
    Note: Upon activating the virtual environment if this error shows up:
    ```
    venv\scripts\activate : File ..\venv\scripts\Activate.ps1 cannot be loaded because running scripts is 
    disabled on this system. For more information, see about_Execution_Policies at http://go.microsoft.com/fwlink/?LinkID=135170.
    ```
    Run this command: 
    ``` 
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted 
    ```
    Then run the command to activate the virtual environment : `venv\scripts\activate`

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database**

   Update `DATABASES` settings in `bookhiveConfig/settings.py` to match your PostgreSQL configuration.

5. **Apply Migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**

   ```bash
   python manage.py runserver
   ```

## API Documentation 📖
Explore the API using the interactive documentation:

- [User Management API Docs 📜](https://bookhiveapi.onrender.com/api/user_mgt/docs)
- [Book Management API Docs 📜](https://bookhiveapi.onrender.com/api/book_mgt/docs)


## Authentication 🔒

### JWT Authentication

- **Generate Token**: POST `/api/token/` with `email` and `password` 🔑
- **Refresh Token**: POST `/api/token/refresh/` with `refresh_token` 🔄

### Example Request for Token Generation

```bash
curl -X POST "https://bookhiveapi.onrender.com/api/user_mgt/login" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### Example Request for Token Refresh

```bash
curl -X POST "https://bookhiveapi.onrender.com/api/token/refresh" -H "Content-Type: application/json" -d '{"refresh_token": "your_refresh_token"}'
```

## Endpoints 📡

### Books 📚

- **List Books**: GET `/api/books/` - List all books.
- **Create Book**: POST `/api/books/` - Create a new book.
- **Retrieve Book**: GET `/api/books/{id}/` - Retrieve a specific book.
- **Update Book**: PUT `/api/books/{id}/` - Update a specific book.
- **Delete Book**: DELETE `/api/books/{id}/` - Delete a specific book.

### Users 👤

- **User Signup**: POST `/api/users/signup/` - Create a new user.
- **User Login**: POST `/api/users/login/` - Login a user.
- **Update User**: PATCH `/api/users/{id}/` - Update user information.
- **Retrieve User**: GET `/api/users/{id}/` - Retrieve a specific user's details.

## Testing 🧪

Run tests using the following command:

```bash
python manage.py test
```

## Error Handling 🚨

Errors are returned in the following format:

```json
{
    "message": "Error message"
}
```

## License 📜

This project is licensed under an [ MIT License](LICENSE).
