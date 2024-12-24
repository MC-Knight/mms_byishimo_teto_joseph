from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where telephone is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, telephone, password, **extra_fields):
        """
        Create and save a User with the given telephone and password.
        """
        if not telephone:
            raise ValueError(_("The Telephone must be set"))
        user = self.model(telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, telephone, password, **extra_fields):
        """
        Create and save a SuperUser with the given telephone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(telephone, password, **extra_fields)
