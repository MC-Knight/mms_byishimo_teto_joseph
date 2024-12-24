import uuid
from django.db import models
from django.conf import settings


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, primary_key=True
    )

    class Meta:
        abstract = True


class Loan(UUIDModel, TimeStampedModel):
    LOAN_STATUS = (
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Declined", "Declined"),
    )

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    monthly_income = models.IntegerField()
    status = models.CharField(max_length=10, choices=LOAN_STATUS, default="Pending")

    def __str__(self):
        return f"{self.user_id.telephone} - {self.amount} - {self.status}"
