from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import UserCreationForm, UserChangeForm
from users.models import User


admin.site.site_header = "MicroLoan Managment System Administration"


class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "first_name",
        "last_name",
        "telephone",
        "user_type",
        "is_active",
    )
    list_filter = (
        "user_type",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("telephone", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        ("Permissions", {"fields": ("user_type", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "telephone",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "user_type",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("telephone",)
    ordering = ("telephone",)


admin.site.register(User, UserAdmin)
