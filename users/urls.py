from django.urls import path

from .views import *

# fmt: off
urlpatterns = [
    path("register", RegisterUserAPIView.as_view()),
    path("login", MyTokenObtainPairView.as_view()),
    path("refresh-token", MyObtainRefreshTokenView.as_view()),
    path("profile", UserDetailAPIView.as_view()),
    path("users", AllUsersDetailAPIView.as_view()),
]
