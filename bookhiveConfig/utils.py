from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

class CustomResponse:
    """A custom response handler for every response sent by the server"""

    @staticmethod
    def success(data=None, message="", status=200) -> JsonResponse:
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
    def failed(data=None, message="", status=400) -> JsonResponse:
        response_data = {
            "status": "failed",
            "data": data or [],
            "message": message
        }
        return JsonResponse(
            response_data,
            status=status
        )

# an utility function to create JWT tokens
def generate_user_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }
