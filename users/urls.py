from django.urls import path
from .views import api as user_api

urlpatterns = [
    path("", user_api.urls),
]
