from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import User
from loan.models import Loan


class LoanListCreateViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", user_type="END_USER"
        )
        self.client.force_authenticate(user=self.user)
        self.loan_url = reverse("loan-list-create")

    def test_get_all_loans(self):
        Loan.objects.create(user_id=self.user, amount=1000, status="PENDING")
        response = self.client.get(self.loan_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("loans", response.data["data"])

    def test_create_loan(self):
        data = {"amount": 1500, "status": "PENDING"}
        response = self.client.post(self.loan_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertIn("loan", response.data["data"])
