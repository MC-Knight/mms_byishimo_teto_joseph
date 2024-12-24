import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        # SYSTEM LEVEL
        ("ADMIN", "ADMIN"),
        # END USER
        ("END_USER", "END_USER"),
    )

    id = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, primary_key=True
    )
    username = None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=10, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "telephone"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    objects = UserManager()

    def __str__(self):
        return (
            f"{self.telephone} - {self.first_name} {self.last_name} - {self.user_type}"
        )
