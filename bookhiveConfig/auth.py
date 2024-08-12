#  this file defines a custom authentication class (using JWT) for my API

from ninja.security import APIKeyHeader
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class JWTAuth(APIKeyHeader):
    def authenticate(self, request):
        # get the Authorization header
        auth_header = request.headers.get("Authorization")

        # check if the header is in the format 'Bearer <token>'
        # and extract the token..
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(' ')[1]
        else:
            return None

        jwt_auth = JWTAuthentication()
        try:
            # authenticate the token
            user, _ = jwt_auth.authenticate(request)
            return user
        except AuthenticationFailed:
            return None
