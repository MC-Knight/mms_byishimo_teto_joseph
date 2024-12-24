from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import *
from .serializers import *
from .permisions import IsAdmin
from pagination.pagination import CustomPagination


@extend_schema(tags=["Auth"])
class RegisterUserAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Override to dynamically set permissions based on user_type
        """
        user_type = self.request.data.get("user_type")

        if user_type == "ADMIN":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]

    def create(self, request, *args, **kwargs):
        user_type = request.data.get("user_type")
        if not self.is_allowed_to_create_user(request.user, user_type):
            raise exceptions.ParseError("You are not allowed to create this user type.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "status": "success",
                "message": "Account created successfully.",
                "data": {
                    "user": UserDetailSerializer(
                        serializer.instance, context=self.get_serializer_context()
                    ).data
                },
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        serializer.save()

    def is_allowed_to_create_user(self, requesting_user, user_type):
        """
        This method checks if the requesting user has the necessary permissions
        to create a user of the given user_type.
        """
        if user_type == "ADMIN":
            return requesting_user.user_type == "ADMIN"
        else:
            return True


@extend_schema(tags=["Auth"])
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


@extend_schema(tags=["Auth"])
class MyObtainRefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)


@extend_schema(tags=["Auth"])
class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(
            {
                "status": "success",
                "message": "User details fetched successfully!",
                "data": {
                    "user": serializer.data,
                },
            }
        )


@extend_schema(tags=["Users"])
class AllUsersDetailAPIView(ListAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserDetailSerializer
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if "data" in response.data and isinstance(response.data["data"], dict):
            paginated_data = response.data["data"]
            formatted_data = {
                "total_records": paginated_data.get("total_count"),
                "total_pages": paginated_data.get("total_pages"),
                "users": paginated_data.get("results"),
                "next": paginated_data.get("next"),
                "previous": paginated_data.get("previous"),
            }
        else:
            formatted_data = {
                "total_pages": 1,
                "users": response.data,
                "next": None,
                "previous": None,
            }

        return Response(
            {
                "status": "success",
                "message": "All users fetched successfully!",
                "data": formatted_data,
            },
            status=status.HTTP_200_OK,
        )
