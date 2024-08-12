from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


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



def get_api():
    """
    Creates and returns a configured instance of NinjaAPI for this project
    """
    from ninja import NinjaAPI
    return NinjaAPI(
        title="BookHive API",
        version="1.0.0",
        description="Welcome to the BookHive API. This API provides endpoints for managing books, users, and related resources.",
    )


