from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListCreateAPIView,
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
)


from .serializers import *
from .models import *
from users.permisions import IsAdmin, IsEndUser
from pagination.pagination import CustomPagination


@extend_schema(tags=["Loan"])
class LoanListCreateView(ListCreateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "status": "success",
                "message": "Loan requested successfully",
                "data": {
                    "loan": serializer.data,
                },
            },
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        queryset = Loan.objects.all()
        user = self.request.user

        if user.user_type == "ADMIN":
            pass
        elif user.user_type == "END_USER":
            queryset = queryset.filter(user_id=user)
        else:
            queryset = queryset.none()
        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(
            user_id=self.request.user,
        )

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        if "data" in response.data and isinstance(response.data["data"], dict):
            paginated_data = response.data["data"]
            formatted_data = {
                "total_records": paginated_data.get("total_count"),
                "total_pages": paginated_data.get("total_pages"),
                "loans": paginated_data.get("results"),
                "next": paginated_data.get("next"),
                "previous": paginated_data.get("previous"),
            }
        else:
            formatted_data = {
                "total_pages": 1,
                "loans": response.data,
                "next": None,
                "previous": None,
            }

        return Response(
            {
                "status": "success",
                "message": "All loans fetched successfully",
                "data": formatted_data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Loan"])
class ChangeLoanStatusView(RetrieveUpdateAPIView):
    serializer_class = ChangeLoanStatusSerializer
    queryset = Loan.objects.all()
    permission_classes = [IsAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "status": "success",
                "message": "Loan status updated successfully",
                "data": {
                    "loan": serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    def perform_update(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response(
            {
                "status": "success",
                "message": "Loan fetched successfully",
                "data": {
                    "loan": response.data,
                },
            },
            status=status.HTTP_200_OK,
        )
