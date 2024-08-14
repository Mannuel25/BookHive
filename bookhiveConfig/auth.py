from ninja import NinjaAPI
from ninja.security import HttpBearer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ninja import Redoc

class BearerAuth(HttpBearer):
    def authenticate(self, request, token: str):
        # verify the token and return the user or raise an error
        user, _ = JWTAuthentication().authenticate(request)
        if not user:
            raise AuthenticationFailed("Invalid token")
        return user


class CustomNinjaAPI(NinjaAPI):
    """
    Extends NinjaAPI to manage both protected and unprotected endpoints
    within a single API instance.
    """

    @staticmethod
    def create_api(title, description, version="1.0.0"):
        return CustomNinjaAPI(
            auth=None, 
            title=title,
            description=description,
            version=version,
            # docs=Redoc()
        )

