import json
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.test import APITestCase, APIClient
from users.models import CustomUser


class CustomResponse:
    """A custom response handler for every response sent by the server"""

    @staticmethod
    def success(data=None, message="success", status=200) -> JsonResponse:
        response_data = {
            "status": "success",
            "data": data or [],
            "message": message
        }
        return JsonResponse(
            response_data,
            status=status
        )

    @staticmethod
    def failed(data=None, message="failed", status=400) -> JsonResponse:
        response_data = {
            "status": "failed",
            "data": data or [],
            "message": message
        }
        return JsonResponse(
            response_data,
            status=status
        )


# an utility function to create JWT for a user
def generate_user_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


# an utility function used to generate a new access 
# token using the provided refresh token
def refresh_access_token(refresh_token: str):
    try:
        # generate a new access token
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return {
            "access": access_token,
            "refresh": str(refresh)
        }
    except (InvalidToken, TokenError) as e:
        raise ValueError(f"Token error: {str(e)}")


class AuthSetupTestCase(APITestCase):
    """
    A test case class for handling authentication setup.

    This class sets up a test client with authenticated credentials, allowing
    derived test cases to interact with the API as an authenticated user. It 
    creates a user and logs them in to obtain an authentication token, which 
    is then used to set the client’s authorization headers for subsequent tests.
    """

    def authenticate(self):
        self.client = APIClient()
        # create a user 
        self.user = CustomUser.objects.create_user(
            email='johh_doe@gmail.com',
            first_name='John',
            last_name='Doe',
            password='John_doe!3',
            is_active=True
        )
        # authenticate the user and get the token
        login_url = "/api/user_mgt/login"
        response = self.client.post(
            login_url,
            data=json.dumps({
                "email": "johh_doe@gmail.com",
                "password": "John_doe!3"
            }),
            content_type='application/json'
        )
        response_data = response.json()
        access_token = response_data.get('data', {}).get('access')
        self.token = f"Bearer {access_token}"
        self.client.credentials(HTTP_AUTHORIZATION=self.token)


