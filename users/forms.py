from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from users.models import User


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=False,
        max_length=50,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter First Name",
                "id": "fname",
            }
        ),
    )
    last_name = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Last Name",
                "id": "lname",
            }
        ),
    )
    telephone = forms.CharField(
        required=False,
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter phone number",
                "id": "phonenumber",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "telephone",
        )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields["telephone"].help_text = "Required. Valid telephone address"

        self.fields["password1"].widget = forms.PasswordInput(
            attrs={"placeholder": _("Create Password"), "id": _("password1")},
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={"placeholder": _("Confirm Password"), "id": _("password2")},
        )

        for fieldname in [
            "first_name",
            "last_name",
            "telephone",
            "password1",
            "password2",
        ]:
            self.fields[fieldname].label = ""


class UserChangeForm(UserChangeForm):
    first_name = forms.CharField(
        max_length=50,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter First Name"}),
    )
    last_name = forms.CharField(
        max_length=50, widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    )
    telephone = forms.CharField(
        max_length=10, widget=forms.TextInput(attrs={"placeholder": "Telephone"})
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "telephone",
        )
