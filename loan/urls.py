from django.urls import path

from .views import *

# fmt: off
urlpatterns = [
    path("loan/", LoanListCreateView.as_view(), name="loan-list-create"),
    path("loan/<uuid:pk>/", ChangeLoanStatusView.as_view(), name="change-loan-status"),
]
