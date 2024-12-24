from django.contrib.auth import authenticate
from rest_framework import serializers, exceptions
from rest_framework.serializers import ModelSerializer
from .models import Loan


class LoanSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "user_id",
            "amount",
            "monthly_income",
            "status",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        if data["amount"] > data["monthly_income"] * 0.3:
            raise exceptions.ParseError(
                "Loan amount can't be more than 30% of monthly income"
            )
        return data


class ChangeLoanStatusSerializer(ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "user_id",
            "amount",
            "monthly_income",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "amount",
            "monthly_income",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user_id",
            "amount",
            "monthly_income",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        if data["status"] not in ["Approved", "Declined"]:
            raise exceptions.ParseError(
                "Loan status can only be 'Approved' or 'Declined'"
            )
        return data
